# -*- coding: utf-8 -*-

"""
sheetsql.exceptions
~~~~~~~~~~~~~~~~~~~~
Exceptions used in sheetsql.
"""


class SheetSQLException(Exception):
    """A base class for sheetsql's exceptions."""

class InvalidSchema(SheetSQLException):
    """Spreadsheet had an invalid schema."""
