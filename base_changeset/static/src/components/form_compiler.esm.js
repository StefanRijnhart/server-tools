/** odoo-module **/

import { FormCompiler } from "@web/views/form/form_compiler.js";
import {patch} from "@web/core/utils/patch";


patch(FormCompiler.prototype, "base_changeset.FormCompiler", {
    setup() {
        super.setup();
        this.insertedChangesetButtons = {};
        this.fieldsWithLabel = [];
    },
    compileNode(node, params = {}, evalInvisible = true) {
        const res = super.compileNode(node, params, evalInvisible);
        if (getTag(node, true) === "field") {
            const addLabel = node.hasAttribute("nolabel")
                  ? node.getAttribute("nolabel") !== "1"
                  : true;
            if (! addLabel) {
                /*
                   Create a changeset button node. If a separate label node is
                   encountered, the node needs to be removed (TODO).
                */
                const button = createElement("BaseChangesetButton", {
                    record: `props.record`,
                    fieldName: node.getAttribuote("name")
                });
                // Store the button in a registry so we can remove it if needed.
                this.insertedChangesetButtons[fieldName] = button;
                //append(
            }
        }
        return res;
    }
});
