# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
import sys, os

version = '0.2.0'

setup(name='Scribbler',
      version=version,
      description="Scribbler is a parallel test runner.",
      long_description="""Introduction
------------

Scribbler is a parallel test runner.

What does it run?
-----------------

Scribbler will pick up any tests where:

* The test method is inside a class
* The test method's name starts with "test\_"

It'll also pick setup methods (methods run before every test) where:

* The setup method is inside a class
* The setup method's name is either "setUp", "setup" or "set_up"

It'll pick teardown methods as well (methods run after every test) where:

* The teardown method is inside a class
* The teardown method's name is either "tearDown", "teardown" or "tear_down"

Will I get any results
----------------------

It's hard for me to spoil the surprise of running, but if you run::

    scribbler_console

Scribbler will try to run all the tests in the current directory (and sub-directories) with the default settings.

For more info on the options run the help with::

    scribbler_console -h

Why Scribbler?
--------------

Ernest Scribbler is the inventor of the Funniest Joke in the World (Monthy Python's sketch).

We love the sketch, hence the name.
      """,
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved",
                   "Natural Language :: English",
                   "Programming Language :: Python :: 2.5", # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
                ],
      keywords='Parallel Testing Python PyUnit',
      author='Bernardo Heynemann',
      author_email='heynemann@gmail.com',
      url='http://github.com/heynemann/scribbler/tree/master',
      license='OSI',
      packages=["scribbler",],
      package_data = {
      },
      include_package_data=False,
      scripts = ['scribbler/scribbler_console.py'],
      zip_safe=True,
      install_requires=[],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
