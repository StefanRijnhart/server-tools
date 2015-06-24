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

{
    'name': 'Inject the form view headers into the form\'s sheet',
    'description': '''
The standard position of the workflow header in OpenERP 7.0 forms is right
below the form's Cancel and Save buttons. This confuses some users. This
module injects this header into the adjacent sheet using an XML view rewrite.

Due to the applied technique of monkey patching, this module may influence
any database on the instance on which it is installed in any other database
although the code takes care only to apply its functionality in database
on which this module is actually installed.

This module is compatible with OpenERP 7.0.
''',
    'version': '7.0.0',
    'author': 'Therp BV',
    'category': 'Usability',
    'website': 'https://therp.nl',
    'license': 'AGPL-3',
    'depends': ['base'],
    'css': ['static/src/css/view_header_to_sheet.css'],
}
