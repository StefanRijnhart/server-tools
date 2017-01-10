# -*- coding: utf-8 -*-
# © 2015 Anubía, soluciones en la nube,SL (http://www.anubia.es)
# © 2017 ONESTEiN BV (http://www.onestein.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Optional CSV import',
    'version': '10.0.1.0.0',
    'category': 'Server tools',
    'summary': 'Group-based permissions for importing CSV files',
    'license': 'AGPL-3',
    'author': 'Odoo Community Association (OCA), '
              'Alejandro Santana <alejandrosantana@anubia.es>, '
              'ONESTEiN BV',
    'maintainer': 'Odoo Community Association (OCA)',
    'website': 'http://odoo-community.org',
    'depends': [
        'web',
        'base_import',
    ],
    'data': [
        'security/base_import_security_group_security.xml',
        'views/base_import.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
