/** @odoo-module */

import {Component} from "@odoo/owl";
import {FormLabel} from "@web/views/form/form_label";
import {FormRenderer} from "@web/views/form/form_renderer";

export class BaseChangesetButton extends Component {
    async onClick(ev) {
        ev.stopPropagation();
        console.log("clicked");
    }
}
BaseChangesetButton.template = "base_changeset.ChangesetButton";

FormLabel.components = FormLabel.components || {};
Object.assign(FormLabel.components, {BaseChangesetButton});
Object.assign(FormRenderer.components, {BaseChangesetButton});
