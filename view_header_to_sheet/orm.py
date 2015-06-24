# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
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
from lxml import etree 
from osv.orm import BaseModel

def fields_view_get(
        self, cr, user, view_id=None, view_type='form',
        context=None, toolbar=False, submenu=False):
    """
    Inject a header in its sibling sheet element on 7.0 forms,
    so that the header buttons are not so close to the save/discard
    buttons.

    As this method is monkeypatched onto BaseModel, check
    if this module is actually installed first.
    """

    result = self.view_header_to_sheet__fields_view_get(
        cr, user, view_id=view_id, view_type=view_type,
        context=context, toolbar=toolbar, submenu=submenu)

    if view_type != 'form':
        return result

    cr.execute("""SELECT id FROM ir_module_module
                  WHERE name = 'view_header_to_sheet'
                  AND state = 'installed'""")
    if not cr.fetchone():
        return result
               
    node = etree.fromstring(result['arch'])
    for header in (
           (node.findall("./header") or []) +
           (node.findall(".//form/header") or [])):

        for sibling in header.find(".."):
            if sibling.tag == 'sheet':
                sibling.insert(0, header)
                break

    result['arch'] = etree.tostring(node)
    return result

BaseModel.view_header_to_sheet__fields_view_get = BaseModel.fields_view_get
BaseModel.fields_view_get = fields_view_get
