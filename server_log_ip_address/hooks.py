# coding: utf-8
# Copyright (C) 2015 Arche TI Inc. - http://www.archeti.ca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime
import logging
import pytz

from openerp.tools import config


def converter(self, timestamp):
    if config['timezone']:
        return datetime.fromtimestamp(timestamp,
                                      pytz.timezone(config['timezone']))
    else:
        return datetime.fromtimestamp(timestamp)


def formatTime(self, record, datefmt=None):
    dt = self.converter(record.created)
    if datefmt:
        s = dt.strftime(datefmt)
    else:
        try:
            t = dt.strftime(self.default_time_format)
        except AttributeError:
            t = dt.strftime("%Y-%m-%d %H:%M:%S")
    try:
        s = self.default_msec_format % (t, record.msecs)
    except AttributeError:
        s = "%s,%03d" % (t, record.msecs)
    return s


def post_load():
    """ Monkeypatch the timestamp formatters """
    logging.Formatter.converter = converter
    logging.Formatter.formatTime = formatTime
