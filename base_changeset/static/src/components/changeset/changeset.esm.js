/** @odoo-module **/

import {FormController} from "@web/views/form/form_controller";
import {FormRenderer} from "@web/views/form/form_renderer";
import {Model} from "@web/views/model";
import {patch} from "@web/core/utils/patch";
import {Popover} from "@web/core/popover/popover";
import {qweb} from "web.core";

patch(Model.prototype, "base_changeset.Model", {
    applyChange(id) {
        return this.orm.call(
            "record.changeset.change",
            "apply",
            [[id]],
            _.extend({}, this.context, {set_change_by_ui: true})
        );
    },

    rejectChange(id) {
        return this.orm.call(
            "record.changeset.change",
            "cancel",
            [[id]],
            _.extend({}, this.context, {set_change_by_ui: true})
        );
    },

    getChangeset(modelName, resId) {
        var self = this;
        return new Promise(function (resolve) {
            return self.orm
                .call("record.changeset.change", "get_fields_changeset_changes", [
                    modelName,
                    resId,
                ])
                .then(function (changeset) {
                    var res = {};
                    _.each(changeset, function (changesetChange) {
                        if (!_.contains(_.keys(res), changesetChange.field_name)) {
                            res[changesetChange.field_name] = [];
                        }
                        res[changesetChange.field_name].push(changesetChange);
                    });
                    resolve(res);
                });
        });
    },
});

patch(FormController.prototype, "base_changeset.FormController", {
    setup() {
        var self = this;
        this._super.apply(this, arguments);
        this._updateChangeset.bind(self);
    },

    // eslint-disable-next-line no-unused-vars
    saveButtonClicked(params = {}) {
        var self = this;
        var res = this._super.apply(this, arguments);
        res.then(function () {
            self._updateChangeset();
        });
        return res;
    },

    beforeLeave() {
        var self = this;
        var res = this._super.apply(this, arguments);
        res.then(function () {
            self._updateChangeset();
        });
        return res;
    },

    beforeUnload(ev) {
        var self = this;
        var res = this._super.apply(this, arguments);
        res.then(function () {
            self._updateChangeset(ev.handle);
        });
        return res;
    },

    // eslint-disable-next-line no-unused-vars
    _updateChangeset(handle) {
        var self = this;
        this.model
            .getChangeset(this.props.resModel, this.props.resId)
            .then(function (changeset) {
                self.props.Renderer.prototype.renderChangesetPopovers(changeset);
            });
    },

    applyChange(id) {
        this.model.applyChange(id).then(this.reload.bind(this));
    },

    rejectChange(id) {
        this.model.rejectChange(id).then(this.reload.bind(this));
    },
});

patch(FormRenderer.prototype, "base_changeset.FormRenderer", {
    renderChangesetPopovers(changeset) {
        var self = this;
        _.each(changeset, function (changes, fieldName) {
            var label = document.querySelector(`label[for=${CSS.escape(fieldName)}]`);
            // If (!$label.length) {
            //     $label = $.find(_.str.sprintf('field[name="%s"]'), fieldName)
            //     if (!$label.length)
            //         return;
            // }
            self._renderChangesetPopover(label, changes);
        });
    },

    htmlToElement(html) {
        var template = document.createElement("template");
        template.innerHTML = html;
        return template.content.firstChild;
    },

    _renderChangesetPopover(label, changes) {
        var self = this;
        var button = this.htmlToElement(
            qweb.render("ChangesetButton", {count: changes.length})
        );
        label.append(button);

        var options = {
            content: function () {
                var content = qweb
                    .render("ChangesetPopover", {changes: changes})
                    .trim();
                content
                    .querySelector(["base_changeset_apply"])
                    .on("click", function () {
                        self._applyClicked(this.data("id"));
                    });
                content
                    .querySelector(["base_changeset_reject"])
                    .on("click", function () {
                        self._rejectClicked(this.data("id"));
                    });
                return content;
            },
            html: true,
            placement: "bottom",
            title: "Pending Changes",
            trigger: "focus",
            delay: {show: 0, hide: 100},
            template: qweb.render("ChangesetTemplate"),
        };

        var popover = new Popover(options);
        label.append(popover);
    },

    _applyClicked: function (rawId) {
        var id = parseInt(rawId, 10);
        this.getParent().applyChange(id);
    },

    _rejectClicked: function (rawId) {
        var id = parseInt(rawId, 10);
        this.getParent().rejectChange(id);
    },
});
