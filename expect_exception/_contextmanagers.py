#!/usr/bin/env python3
"""Context managers for expect_exception."""

import contextlib

from typing import Any, Optional, Type

from ._enums import Status
from ._errors import ExceptionNotRaisedError


class _ExpectedException(contextlib.AbstractContextManager,
                         contextlib.ContextDecorator):
  """Context manager that expects code to raise an exception."""

  def __init__(self,
               *exception_types: Type[BaseException],
               wrap_unexpected_exception: bool = True):
    """Context manager that expects code to raise an exception.

    Args:
      *exception_types: one or more exception types (class objects) that are
        expected to be raised in this context. Exceptions that inherit from any
        of those listed here will also be caught.
      wrap_unexpected_exception: True to wrap any unexpected exception in an
        ExceptionNotRaisedError; False to bubble up the unexpected exception.
        Defaults to True.
    """
    if not exception_types:
      raise ValueError('At least one BaseException type must be provided')
    if any(not isinstance(exception_type, type) or
           not issubclass(exception_type, BaseException)
           for exception_type in exception_types):
      raise TypeError(
          'All exception_types arguments must be sub-type of BaseException')

    self._expected_exception_types = exception_types
    self._wrap_unexpected_exception = wrap_unexpected_exception
    self._status = Status.PENDING
    self._exception = None

  def __enter__(self):
    return self

  def __exit__(self, exception_type: Optional[Type[BaseException]],
               exception_value: Optional[BaseException], unused_traceback: Any):
    self._exception = exception_value

    if exception_type is None:
      self._status = Status.UNEXPECTED_EXECUTION_COMPLETED
      raise ExceptionNotRaisedError(None, self._status)

    if any(
        issubclass(exception_type, expected_exception_type)
        for expected_exception_type in self._expected_exception_types):
      self._status = Status.EXPECTED_EXCEPTION_RAISED
      return True

    self._status = Status.UNEXPECTED_EXCEPTION_RAISED
    if self._wrap_unexpected_exception:
      raise ExceptionNotRaisedError(exception_value, self._status)
    return False

  @property
  def status(self) -> Status:
    return self._status

  @property
  def exception(self) -> Optional[BaseException]:
    return self._exception
