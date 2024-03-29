"""
Custom exceptions raised by modules
"""


class DuplicatePlayerError(Exception):
    pass


class BracketPlayerCount(Warning):
    pass


class BracketAssignmentError(Exception):
    pass
