/** @odoo-module **/

import {createElement, getTag} from "@web/core/utils/xml";
import {FormCompiler} from "@web/views/form/form_compiler";
import {patch} from "@web/core/utils/patch";

patch(FormCompiler.prototype, "base_changeset.FormCompiler", {
    setup() {
        this._super.apply(this, arguments);
        this.insertedChangesetButtons = {};
        this.fieldsWithLabel = [];
    },
    compileField(el, params) {
        let nodes = this._super.apply(this, arguments);
        nodes = Array.isArray(nodes) ? nodes : [nodes];
        const inInnerGroup = getTag(el.parentNode) === "group" && getTag(el.parentNode.parentNode) === "group";
        const hasLabel = (
            el.nodeType !== Node.TEXT_NODE
                && inInnerGroup
                && (
                    el.hasAttribute("nolabel")
                        ? el.getAttribute("nolabel") !== "1"
                        : true
                )
        );
        if (!hasLabel) {
            /*
              Append a changeset button node after the field node.
              If a separate label node is
              encountered, the node needs to be removed (TODO).
            */
            const fieldName = el.getAttribute("name");
            const button = createElement("BaseChangesetButton", {
                record: `props.record`,
                fieldName: fieldName,
            });
            // Store the button in a registry so we can remove it if needed.
            this.insertedChangesetButtons[fieldName] = button;

            console.log("Attach to field: " + el.getAttribute("name"));
            nodes.push(button);
        }
        return nodes;
    },
});
