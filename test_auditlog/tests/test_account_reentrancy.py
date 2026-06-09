from odoo.tests.common import tagged

from odoo.addons.auditlog.tests.common import AuditLogRuleCommon


@tagged("post_install", "-at_install")
class TestAccountAuditlog(AuditLogRuleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.account_model_id = cls.env.ref("account.model_account_account").id

        cls.rule = cls.create_rule(
            {
                "name": "Account Audit Rule",
                "model_id": cls.account_model_id,
                "log_create": True,
                "log_write": True,
                "log_read": True,
                "log_unlink": True,
                "log_type": "full",
            }
        )
        cls.rule.set_to_confirmed()

    def test_write_code_reentrancy(self):
        account = self.env["account.account"].create(
            {
                "name": "Test Account",
                "code": "1000",
            }
        )

        logs = self.env["auditlog.log"].search(
            [
                ("model_id", "=", self.account_model_id),
                ("method", "=", "write"),
                ("res_id", "=", account.id),
            ]
        )

        self.assertTrue(
            logs.line_ids.filtered(lambda log_line: log_line.field_name == "code_store")
        )

        account.write({"code": "2000"})

        logs = self.env["auditlog.log"].search(
            [
                ("model_id", "=", self.account_model_id),
                ("method", "=", "write"),
                ("res_id", "=", account.id),
            ]
        )

        self.assertEqual(len(logs), 2)
