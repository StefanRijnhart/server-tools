# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Conditional attachments on email templates',
    'version': '0.1',
    'author': 'Therp BV,Odoo Community Assocation (OCA)',
    'category': 'Email',
    'license': 'AGPL-3',
    'website': 'http://therp.nl',
    'depends': [
        'email_template',
        ],
    'data': [
        'view/email_template.xml',
        'view/ir_attachment.xml',
        'security/ir.model.access.csv',
        ],
    'description': """
This module allows you to configure a set of static attachments on an email
template that appear on generated emails conditionally. Conditions are
specified in the technical *domain* notation that is widely used in OpenERP.

For instance, if you want
a specific attachment to only be sent out with invoices to Dutch speaking
customers of a specific company, you can encode this on the template for
outgoing invoices as a regular domain expression against the invoice model:

    [('company_id', '=', 1), ('partner_id.lang', '=', 'nl_NL')]

Generated emails will then only contain the attachment if the associated
invoice meets these requirements.

You can configure the conditional attachments on the *Advanced* tab of the
email template form view.

Again, only static attachments (so no dynamically generated reports) are
currently supported. An example of usage is attaching a document containing
general terms and conditions in various languages which can vary per company
or customer region.
""",
}
