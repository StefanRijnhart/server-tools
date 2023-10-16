import copy
from collections import defaultdict

from odoo import api, models
from odoo.tools import ormcache


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _get_auditlog_rule(self, mode):
        """Fetch the relevant auditlog rule for this model and the given operation."""
        model2rule = self._fetch_auditlog_rules()
        rule_id = model2rule[self._name].get(mode)
        if rule_id:
            rule = self.env["auditlog.rule"].sudo().browse(rule_id)
            if self.env.user not in rule.users_to_exclude_ids:
                return rule
        return self.env["auditlog.rule"].sudo()

    @api.model
    @ormcache()
    def _fetch_auditlog_rules(self):
        """Fetch a cache with the full auditlog configuration.

        Also populate the "model name to model id" cache.
        """
        if not hasattr(self.pool, "_auditlog_model_cache"):
            self.pool._auditlog_model_cache = {}
        model2rule = defaultdict(dict)
        for rule in (
            self.env["auditlog.rule"].sudo().search([("state", "=", "subscribed")])
        ):
            self.pool._auditlog_model_cache[rule.model_id.model] = rule.model_id.id
            for method in ("create", "read", "unlink", "write"):
                if rule["log_%s" % method]:
                    model2rule[rule.model_id.model][method] = rule.id
        return model2rule

    @api.model_create_multi
    def create(self, vals_list):
        """Apply auditlog rules when creating records."""
        rule = self._get_auditlog_rule("create")
        if rule:
            if rule.log_type == "fast":
                vals_list = rule._update_vals_list(vals_list)
                vals_list2 = copy.deepcopy(vals_list)
            self = self.with_context(auditlog_disable=True)
        new_records = super().create(vals_list)
        if rule:
            new_values = {}
            if rule.log_type == "full":
                # Take a snapshot of record values from the cache instead of using
                # 'read()'. It avoids issues with related/computed fields which
                # stored in the database only at the end of the transaction, but
                # their values exist in cache.
                fields_list = rule.get_auditlog_fields(self)
                for new_record in new_records.sudo():
                    new_values.setdefault(new_record.id, {})
                    for fname, field in new_record._fields.items():
                        if fname not in fields_list:
                            continue
                        new_values[new_record.id][fname] = field.convert_to_read(
                            new_record[fname], new_record
                        )
            else:
                for vals, new_record in zip(vals_list2, new_records):
                    new_values.setdefault(new_record.id, vals)
            rule.create_logs(
                self.env.uid,
                self._name,
                new_records.ids,
                "create",
                None,
                new_values,
                {"log_type": rule.log_type},
            )
        return new_records

    def read(self, fields=None, load="_classic_read", **kwargs):
        """Apply auditlog rules when reading records."""
        result = super().read(fields, load=load, **kwargs)
        rule = self._get_auditlog_rule("read")
        # If the call came from auditlog itself, skip logging:
        # avoid logs on `read` produced by auditlog during internal
        # processing: read data of relevant records, 'ir.model',
        # 'ir.model.fields'... (no interest in logging such operations)
        if rule and not self.env.context.get("auditlog_disabled"):
            # Sometimes the result is not a list but a dictionary
            # Also, we can not modify the current result as it will break calls
            result2 = result
            if not isinstance(result2, list):
                result2 = [result]
            read_values = {d["id"]: d for d in result2}
            self = self.with_context(auditlog_disabled=True)
            rule.create_logs(
                self.env.uid,
                self._name,
                self.ids,
                "read",
                read_values,
                None,
                {"log_type": rule.log_type},
            )
        return result

    def write(self, vals):
        """Apply auditlog rules when writing records."""
        rule = self._get_auditlog_rule("write")
        if rule:
            self = self.with_context(auditlog_disabled=True)
            if rule.log_type == "full":
                fields_list = rule.get_auditlog_fields(self)
                old_values = {
                    d["id"]: d
                    for d in self.sudo()
                    .with_context(prefetch_fields=False)
                    .read(fields_list)
                }
            else:
                vals2 = dict(vals)
                old_vals2 = dict.fromkeys(list(vals2.keys()), False)
                old_values = {id_: old_vals2 for id_ in self.ids}
                new_values = {id_: vals2 for id_ in self.ids}
        result = super().write(vals)
        if rule:
            if rule.log_type == "full":
                new_values = {
                    d["id"]: d
                    for d in self.sudo()
                    .with_context(prefetch_fields=False)
                    .read(fields_list)
                }
            rule.create_logs(
                self.env.uid,
                self._name,
                self.ids,
                "write",
                old_values,
                new_values,
                {"log_type": rule.log_type},
            )
        return result

    def unlink(self):
        """Apply auditlog rules when unlinking records."""
        rule = self._get_auditlog_rule("unlink")
        if rule:
            self = self.with_context(auditlog_disabled=True)
            if rule.log_type == "full":
                fields_list = rule.get_auditlog_fields(self)
                old_values = {
                    d["id"]: d
                    for d in self.sudo()
                    .with_context(prefetch_fields=False)
                    .read(fields_list)
                }
            else:
                old_values = None
            rule.create_logs(
                self.env.uid,
                self._name,
                self.ids,
                "unlink",
                old_values,
                None,
                {"log_type": rule.log_type},
            )
        return super().unlink()
