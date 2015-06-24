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
from ast import literal_eval
from openerp.osv import orm, fields


class EmailTemplate(orm.Model):
    _inherit = 'email.template'
    _columns = {
        'conditional_attachment_ids': fields.one2many(
            'email.template.conditional.attachment',
            'template_id', 'Conditional attachments'),
        }

    def generate_email(self, cr, uid, template_id, res_id, context=None):
        """
        Go through the conditional attachments and select those
        of which the domain matches the resource.
        """
        res = super(EmailTemplate, self).generate_email(
            cr, uid, template_id, res_id, context=context)
        if res_id:
            template = self.browse(cr, uid, template_id, context=context)
            for attachment in template.conditional_attachment_ids:
                domain = (
                    ['&', ('id', '=', res_id)] +
                    literal_eval(attachment.domain))
                if self.pool.get(template.model).search(
                        cr, uid, domain, context=context):
                    res['attachment_ids'].append(
                        attachment.attachment_id.id)
        return res
            
