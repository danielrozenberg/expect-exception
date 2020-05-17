#!/usr/bin/env python3
"""Context manager that expects code to raise an exception."""

from ._contextmanagers import _ExpectedException
from ._enums import Status
from ._errors import ExceptionNotRaisedError

expect_exception = _ExpectedException  # pylint: disable=invalid-name
