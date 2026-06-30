# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

GUARD_CONTEXT_KEY = "auditlog_guard"


def add_guard(records, keys):
    """Return a copy of ``records`` whose context tracks the given guard keys.

    The guard is stored in the context so that it is propagated to the nested
    operations triggered by the write (e.g. recomputation of stored computed
    fields) and naturally discarded once the recordset goes out of scope.
    """
    guard = set(records.env.context.get(GUARD_CONTEXT_KEY, ()))
    guard.update(keys)
    return records.with_context(**{GUARD_CONTEXT_KEY: frozenset(guard)})


def has_conflict(records, keys):
    """Return whether all the given guard keys are already being processed.

    Keys carry a field dimension (model, ids, field), so a nested write is only
    considered a recursion when every field it writes is already guarded.
    Nested writes touching other fields are still logged.
    """
    guard = records.env.context.get(GUARD_CONTEXT_KEY, frozenset())
    return bool(keys) and set(keys) <= set(guard)
