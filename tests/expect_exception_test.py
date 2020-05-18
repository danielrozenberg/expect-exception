#!/usr/bin/env python3
"""Unit tests for expect_exception."""

import unittest

from expect_exception import *


class ExpectExceptionTest(unittest.TestCase):
  """Unit tests for expect_exception."""

  def test_expected_exception(self):
    with expect_exception(ZeroDivisionError) as ee:
      self.assertEqual(Status.PENDING, ee.status)
      return 1 / 0

    self.assertEqual(Status.EXPECTED_EXCEPTION_RAISED, ee.status)
    self.assertIsInstance(ee.exception, ZeroDivisionError)

  def test_expected_multiple_exception(self):
    with expect_exception(IndexError, ZeroDivisionError) as ee:
      return 1 / 0

    self.assertEqual(Status.EXPECTED_EXCEPTION_RAISED, ee.status)
    self.assertIsInstance(ee.exception, ZeroDivisionError)

  def test_expected_parent_exception(self):
    with expect_exception(ArithmeticError) as ee:
      return 1 / 0

    self.assertEqual(Status.EXPECTED_EXCEPTION_RAISED, ee.status)
    self.assertIsInstance(ee.exception, ZeroDivisionError)

  def test_fail_on_no_exception_types(self):
    with self.assertRaisesRegex(ValueError, 'At least one'):
      with expect_exception():
        pass

  def test_fail_on_non_exception_type(self):
    with self.assertRaisesRegex(TypeError, 'must be sub-type of BaseException'):
      with expect_exception(tuple):  # type: ignore
        pass

  def test_fail_on_none_exception_type(self):
    with self.assertRaisesRegex(TypeError, 'must be sub-type of BaseException'):
      with expect_exception(None):  # type: ignore
        pass

  def test_fail_on_exception_instance(self):
    with self.assertRaisesRegex(TypeError, 'must be sub-type of BaseException'):
      with expect_exception(ZeroDivisionError()):  # type: ignore
        pass

  def test_unexpected_exception(self):
    with self.assertRaises(ExceptionNotRaisedError) as enre:
      with expect_exception(ZeroDivisionError) as ee:
        numbers = [0, 7, 42]
        numbers[3] += 1

    self.assertEqual(Status.UNEXPECTED_EXCEPTION_RAISED, enre.exception.status)
    self.assertEqual(Status.UNEXPECTED_EXCEPTION_RAISED, ee.status)
    self.assertIs(enre.exception.exception, ee.exception)
    self.assertIsInstance(ee.exception, IndexError)

  def test_unexpected_execution_completed(self):
    with self.assertRaises(ExceptionNotRaisedError) as enre:
      with expect_exception(ZeroDivisionError) as ee:
        pass

    self.assertEqual(Status.UNEXPECTED_EXECUTION_COMPLETED,
                     enre.exception.status)
    self.assertEqual(Status.UNEXPECTED_EXECUTION_COMPLETED, ee.status)
    self.assertIsNone(ee.exception)

  def test_unwrapped_expected_exception(self):
    with expect_exception(ZeroDivisionError,
                          wrap_unexpected_exception=False) as ee:
      return 1 / 0

    self.assertEqual(Status.EXPECTED_EXCEPTION_RAISED, ee.status)
    self.assertIsInstance(ee.exception, ZeroDivisionError)

  def test_unwrapped_unexpected_exception(self):
    with self.assertRaises(IndexError) as ie:
      with expect_exception(ZeroDivisionError,
                            wrap_unexpected_exception=False) as ee:
        numbers = [0, 7, 42]
        numbers[3] += 1

    self.assertEqual(Status.UNEXPECTED_EXCEPTION_RAISED, ee.status)
    self.assertIs(ie.exception, ee.exception)
    self.assertIsInstance(ee.exception, IndexError)

  def test_unwrapped_unexpected_execution_completed(self):
    with self.assertRaises(ExceptionNotRaisedError):
      with expect_exception(ZeroDivisionError,
                            wrap_unexpected_exception=False) as ee:
        pass

    self.assertEqual(Status.UNEXPECTED_EXECUTION_COMPLETED, ee.status)
    self.assertIsNone(ee.exception)

  def test_decorator_expected_exception(self):  # pylint: disable=no-self-use

    @expect_exception(ZeroDivisionError)
    def divide_by_zero():
      return 1 / 0

    divide_by_zero()

  def test_decorator_unexpected_exception(self):

    @expect_exception(IndexError)
    def divide_by_zero():
      return 1 / 0

    with self.assertRaises(ExceptionNotRaisedError) as enre:
      divide_by_zero()

    self.assertEqual(Status.UNEXPECTED_EXCEPTION_RAISED, enre.exception.status)
    self.assertIsInstance(enre.exception.exception, ZeroDivisionError)

  def test_decorator_unwrapped_unexpected_exception(self):

    @expect_exception(IndexError, wrap_unexpected_exception=False)
    def divide_by_zero():
      return 1 / 0

    with self.assertRaises(ZeroDivisionError):
      divide_by_zero()

  def test_decorator_unexpected_execution_completed(self):

    @expect_exception(ZeroDivisionError)
    def divide_by_one():
      return 1 / 1

    with self.assertRaises(ExceptionNotRaisedError) as enre:
      divide_by_one()

    self.assertEqual(Status.UNEXPECTED_EXECUTION_COMPLETED,
                     enre.exception.status)
    self.assertIsNone(enre.exception.exception)


if __name__ == '__main__':
  unittest.main()
