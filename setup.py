#!/usr/bin/env python3
"""Context manager that expects code to raise an exception."""

import setuptools

with open('README.md', 'r') as f:
  long_description = f.read()

setuptools.setup(
    name='expect-exception',
    version='1.0.1',
    author='Daniel Rozenberg',
    author_email='me@danielrozenberg.com',
    description='Context manager that expects code to raise an exception',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/danielrozenberg/expect-exception',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Typing :: Typed',
    ],
    python_requires='>=3.6',
    platforms=['any'],
    license='ISC',
)
