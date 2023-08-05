#!/usr/bin/env python

import os

from setuptools import setup

from dsprpc import __version__

def long_description():
  os.system('pandoc --from=markdown --to=rst --output=README.rst README.md')
  readme_fn = os.path.join(os.path.dirname(__file__), 'README.rst')
  if os.path.exists(readme_fn):
    with open(readme_fn) as f:
      return f.read()
  else:
    return 'not available'

setup(name='dsprpc',
  version=__version__,
  description="A simple, no-setup Python PRC",
  long_description=long_description(),
  author='Derek Anderson',
  author_email='public@kered.org',
  url='https://github.com/keredson/dsprpc',
  py_modules=['dsprpc'],
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
  ],
)
