/** @odoo-module **/

import {createElement, getTag} from "@web/core/utils/xml";
import {FormCompiler} from "@web/views/form/form_compiler";
import {copyAttributes} from "@web/views/view_compiler";
import {patch} from "@web/core/utils/patch";

patch(FormCompiler.prototype, "base_changeset.FormCompiler", {
    setup() {
        this._super.apply(this, arguments);
        this.insertedChangesetButtons = {};
        this.fieldsWithLabel = [];
    },
    appendChangesetButtons(el, params) {
        for (const child of el.children) {
            console.log(getTag(child));
            if (getTag(child) === "Field") {
                // FIXME do not carry group tag at this point
                const inInnerGroup =
                    getTag(child.parentNode) === "group" &&
                    getTag(child.parentNode.parentNode) === "group";
                const hasLabel =
                    child.nodeType !== Node.TEXT_NODE &&
                    inInnerGroup &&
                    (child.hasAttribute("nolabel")
                        ? child.getAttribute("nolabel") !== "1"
                        : true);
                if (!hasLabel) {
                    /*
                      Append a changeset button node after the field node.
                      If a separate label node is
                      encountered, the node needs to be removed (TODO).
                    */
                    const fieldName = child.getAttribute("name");
                    const button = createElement("BaseChangesetButton", {
                        record: `props.record`,
                        fieldName: fieldName,
                    });
                    button.setAttribute(
                        "Component",
                        "constructor.components.FormLabel"
                    );
                    button.setAttribute("subType", "'item_component'");
                    // Store the button in a registry so we can remove it if needed.
                    const button_node = this.compileNode(button, params);
                    copyAttributes(child, button_node);
                    this.insertedChangesetButtons[fieldName] = button;
                    console.log("Attach to field: " + fieldName);
                    child.after(button_node);
                }
            } else {
                this.appendChangesetButtons(child);
            }
        }
    },
    compile(key, params = {}) {
        const compiled = this._super.apply(this, arguments);
        this.appendChangesetButtons(compiled, params);
        return compiled;
    },
});
