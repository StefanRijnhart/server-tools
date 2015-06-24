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
from openerp.osv import orm, fields


class EmailTemplateConditionalAttachment(orm.Model):
    _name = 'email.template.conditional.attachment'
    
    _columns = {
        'template_id': fields.many2one(
            'email.template', 'Email template', required=True,
            ondelete='CASCADE'),
        'attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', required=True),
        'domain': fields.char(
            size=256, string='Domain', required=True),
        }
