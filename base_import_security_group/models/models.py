# -*- coding: utf-8 -*-
# © 2015 Anubía, soluciones en la nube,SL (http://www.anubia.es)
# © 2017 ONESTEiN BV (http://www.onestein.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api
from openerp.models import BaseModel
import logging

_logger = logging.getLogger(__name__)
base_load = BaseModel.load


@api.model
def load_import_optional(self, fields=None, data=None):
    '''Overriding this method we only allow its execution
    if current user belongs to the group allowed for CSV data import.
    An exception is raised otherwise, and also log the import attempt.
    '''
    current_user = self.env['res.users'].browse(self.env.uid)
    allowed_group = 'base_import_security_group.group_import_csv'
    allowed_group_id = self.env.ref(
        'base_import_security_group.group_import_csv', raise_if_not_found=False)
    if not allowed_group_id or \
            (current_user and current_user.has_group(allowed_group)):
        res = base_load(self, fields=fields, data=data)
    else:
        msg = ('User (ID: %s) is not allowed to import data '
               'in model %s.') % (self.env.uid, self._name)
        _logger.error(msg)
        messages = []
        info = {}
        messages.append(dict(info, type='error', message=msg, moreinfo=None))
        res = {'ids': None, 'messages': messages}
    return res


# Monkey patch function
# A Because BaseModel _name = None
BaseModel.load = load_import_optional
