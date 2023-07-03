/** @odoo-module **/

import {qweb} from "web.core";
import BasicModel from "web.BasicModel";
import {FormController} from "@web/views/form/form_controller";
import {FormRenderer} from "@web/views/form/form_renderer";

export class ChangeSetBasicModel extends BasicModel {
    applyChange(id) {
        return this._rpc({
            model: "record.changeset.change",
            method: "apply",
            args: [[id]],
            context: _.extend({}, this.context, {set_change_by_ui: true}),
        });
    }

    rejectChange(id) {
        return this._rpc({
            model: "record.changeset.change",
            method: "cancel",
            args: [[id]],
            context: _.extend({}, this.context, {set_change_by_ui: true}),
        });
    }

    getChangeset(modelName, resId) {
        var self = this;
        return new Promise(function (resolve) {
            return self
                ._rpc({
                    model: "record.changeset.change",
                    method: "get_fields_changeset_changes",
                    args: [modelName, resId],
                })
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
    }
}

export class ChangeSetFormController extends FormController {
    start() {
        return this._super
            .apply(this, arguments)
            .then(this._updateChangeset.bind(this));
    }

    update() {
        var self = this;
        var res = this._super.apply(this, arguments);
        res.then(function () {
            self._updateChangeset();
        });
        return res;
    }

    _updateChangeset() {
        var self = this;
        var state = this.model.get(this.handle);
        this.model.getChangeset(state.model, state.data.id).then(function (changeset) {
            self.renderer.renderChangesetPopovers(changeset);
        });
    }

    applyChange(id) {
        this.model.applyChange(id).then(this.reload.bind(this));
    }

    rejectChange(id) {
        this.model.rejectChange(id).then(this.reload.bind(this));
    }
}

export class ChangeSetFormRenderer extends FormRenderer {
    renderChangesetPopovers(changeset) {
        var self = this;
        _.each(changeset, function (changes, fieldName) {
            var labelId = self._getIDForLabel(fieldName);
            var $label = self.$el.find(_.str.sprintf('label[for="%s"]', labelId));
            if (!$label.length) {
                var widgets = _.filter(
                    self.allFieldWidgets[self.state.id],
                    function (widget) {
                        return widget.name === fieldName;
                    }
                );
                if (widgets.length === 1) {
                    var widget = widgets[0];
                    $label = widget.$el;
                } else {
                    return;
                }
            }
            self._renderChangesetPopover($label, changes);
        });
    }

    _renderChangesetPopover($el, changes) {
        var self = this;
        if (this.mode !== "readonly") {
            return;
        }
        var $button = $(
            qweb.render("ChangesetButton", {
                count: changes.length,
            })
        );

        $el.append($button);

        var options = {
            content: function () {
                var $content = $(
                    qweb.render("ChangesetPopover", {
                        changes: changes,
                    })
                );
                $content.find(".base_changeset_apply").on("click", function () {
                    self._applyClicked($(this));
                });
                $content.find(".base_changeset_reject").on("click", function () {
                    self._rejectClicked($(this));
                });
                return $content;
            },
            html: true,
            placement: "bottom",
            title: "Pending Changes",
            trigger: "focus",
            delay: {show: 0, hide: 100},
            template: qweb.render("ChangesetTemplate"),
        };

        $button.popover(options);
    }

    _applyClicked($el) {
        var id = parseInt($el.data("id"), 10);
        this.getParent().applyChange(id);
    }

    _rejectClicked($el) {
        var id = parseInt($el.data("id"), 10);
        this.getParent().rejectChange(id);
    }
}
