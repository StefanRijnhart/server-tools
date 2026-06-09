# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import threading

_auditlog_local = threading.local()


def get_guard():
    if not hasattr(_auditlog_local, "guard"):
        _auditlog_local.guard = set()
    return _auditlog_local.guard


def add_guard(keys):
    guard = get_guard()
    guard.update(keys)
    return guard


def has_conflict(keys):
    guard = get_guard()
    return bool(guard.intersection(keys))


def remove_guard(keys):
    guard = get_guard()
    guard.difference_update(keys)
