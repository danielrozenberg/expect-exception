#!/usr/bin/env python3
"""Enums for expect_exception."""

import enum


class Status(enum.Enum):
  """Status of the expect_exception context."""

  # The code within the context is still executing.
  PENDING = 0

  # The code within the context raised the expected exception.
  EXPECTED_EXCEPTION_RAISED = 1

  # The code within the context raised an unexpected exception.
  UNEXPECTED_EXCEPTION_RAISED = 2

  # The code within the context completed without raising an exception.
  UNEXPECTED_EXECUTION_COMPLETED = 3
