#!/usr/bin/env python


class ObtConflictError(Exception):
    pass


class ObtMissError(Exception):
    pass


class NoEnoughDpvError(Exception):
    pass


class DpvError(Exception):
    pass


class ThostError(Exception):
    pass


class DlvStatusError(Exception):
    pass


class FjStatusError(Exception):
    pass


class HasFjError(Exception):
    pass


class ThinMaxRetryError(Exception):
    pass


class SnapshotStatusError(Exception):
    pass


class DeleteActiveSnapshotError(Exception):
    pass


class SnapNameError(Exception):
    pass


class ApiError(Exception):
    pass


class FsmFailed(Exception):
    pass


class DlvThostMisMatchError(Exception):
    pass
