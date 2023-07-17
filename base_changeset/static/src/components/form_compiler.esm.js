/** @odoo-module **/

import {FormCompiler} from "@web/views/form/form_compiler";
import {append, createElement, getTag} from "@web/core/utils/xml";
import {patch} from "@web/core/utils/patch";

patch(FormCompiler.prototype, "base_changeset.FormCompiler", {
    setup() {
        this._super.apply(this, arguments);
        this.insertedChangesetButtons = {};
        this.fieldsWithLabel = [];
    },
    compileNode(node, params = {}, evalInvisible = true) {
        const res = this._super.apply(this, arguments);
        if (getTag(node, true) == "field") {
            if (node.getAttribute("name") == "zip") {
                console.log("debug me");
            }
            const addLabel = node.hasAttribute("nolabel")
                ? node.getAttribute("nolabel") !== "1"
                : true;
            if (!addLabel) {
                /*
                   Create a changeset button node. If a separate label node is
                   encountered, the node needs to be removed (TODO).
                */
                const fieldName = node.getAttribute("name");
                const button = createElement("BaseChangesetButton", {
                    record: `props.record`,
                    fieldName: fieldName,
                });
                // Store the button in a registry so we can remove it if needed.
                this.insertedChangesetButtons[fieldName] = button;
                // Append(
            }
        }
        return res;
    },
});
