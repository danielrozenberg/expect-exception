# expect-exception

A decorator and context manager to run code that you expect (and want!) to raise
an exception.

This module is meant to "reverse" the usage of `try/except`, for when you write
code where the exception is the "good" branch. It raises an
`ExceptionNotRaisedError` when the expected exception type is not raised in the
wrapped code, either because it finished executing or because another,
unexpected exception was raised.

For example, you can use `expect_exception` to replace the following code:

```python
def upload_new_file(filename, content)
  try:
    some_api.fetch_file(filename)
  except FileNotFoundError:
    # We don't want to override existing files on SomeService, but SomeApi
    # doesn't have a method to check if a file exists!
    pass

  some_api.upload_file(filename, content)
```

With this:

```python
def upload_new_file(filename, content)
  with expect_exception(FileNotFoundError):
    # We don't want to override existing files on SomeService, but SomeApi
    # doesn't have a method to check if a file exists!
    some_api.fetch_file(filename)
  some_api.upload_file(filename, content)
```

Alternatively, you can use `expect_exception` as a decorator for a helper
method:

```python
# some_api.py

class SomeApi(...):
  ...

  def fetch_file(self, filename):
    ...

  @expect_exception(FileNotFoundError):
  def ensure_file_missing(self, filename):
    self.fetch_file(filename)

# ---

def upload_new_file(filename, content):
  some_api.ensure_file_missing(filename)
  some_api.upload_file(filename, content)
```

## Usage

```python
from expect_exception import expect_exception

# Use either as a @decorator or as a `with` statement context.
expect_exception(
  SomeExceptionType[, SomeExceptionType, ...,
  wrap_unexpected_exception: bool])
```

Arguments:

- `*exception_types: Type[BaseException]` (positional arguments): one or more
  exception types (class objects) that are expected to be raised in this
  context.
  Exceptions that inherit from any of those listed here will also be caught.
- `wrap_unexpected_exception: bool` (keyword only argument): True to wrap any
  unexpected exception in an `ExceptionNotRaisedError`; False to bubble up the
  unexpected exception.
  Defaults to True.
