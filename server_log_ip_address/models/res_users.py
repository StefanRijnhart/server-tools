# -*- coding: utf-8 -*-
# Copyright (C) 2015 Arche TI Inc. - http://www.archeti.ca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openerp import models
from openerp.http import request


_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def _get_ipaddress(self):
        if request:
            if 'HTTP_X_FORWARDED_FOR' in request.httprequest.environ:
                ip_adds = request.httprequest.environ[
                    'HTTP_X_FORWARDED_FOR'].split(",")
                ip = ip_adds[0]
            else:
                ip = request.httprequest.environ['REMOTE_ADDR']
        else:
            ip = '<unknown>'
        return ip

    def _get_log_info(self, db, login, msg):
        msg = "%s from %s using database %s with IP address: %s " \
            % (msg, login, db, self._get_ipaddress())
        _logger.info(msg)
        return True

    def _login(self, db, login, password):
        """ Log login attempts """
        user_id = super(ResUsers, self)._login(db, login, password)
        if user_id:
            self._get_log_info(db, login, 'Login Successfully')
        else:
            self._get_log_info(db, login, 'Login Failed')
        return user_id
