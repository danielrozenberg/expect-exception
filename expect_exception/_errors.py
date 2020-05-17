#!/usr/bin/env python3
"""Error types for expect_exception."""

from typing import Optional

from ._enums import Status


class ExceptionNotRaisedError(RuntimeError):
  """An expected exception was not raised."""

  def __init__(self, exception: Optional[BaseException], status: Status, *args):
    super().__init__(*args)
    self._exception = exception
    self._status = status

  @property
  def status(self) -> Status:
    return self._status

  @property
  def exception(self) -> Optional[BaseException]:
    """Returns the unexpected exception if one was raised, None otherwise."""
    return self._exception
