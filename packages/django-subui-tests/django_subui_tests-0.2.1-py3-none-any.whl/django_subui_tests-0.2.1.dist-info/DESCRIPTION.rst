==================
Django SubUI Tests
==================

.. image:: https://badge.fury.io/py/django-subui-tests.png
    :target: http://badge.fury.io/py/django-subui-tests

.. image:: https://travis-ci.org/dealertrack/django-subui-tests.png?branch=master
    :target: https://travis-ci.org/dealertrack/django-subui-tests

.. image:: https://coveralls.io/repos/dealertrack/django-subui-tests/badge.png?branch=master
    :target: https://coveralls.io/r/dealertrack/django-subui-tests?branch=master

Framework to make workflow server integration test suites

* Free software: MIT license
* GitHub: https://github.com/dealertrack/django-subui-tests
* Documentation: http://django-subui-tests.readthedocs.io/

Installing
----------

You can install ``django-subui-tests`` using pip::

    $ pip install django-subui-tests

Testing
-------

To run the tests you need to install testing requirements first::

    $ make install

Then to run tests, you can use ``nosetests`` or simply use Makefile command::

    $ nosetests -sv
    # or
    $ make test




History
-------

0.2.1 (2017-4-26)
-----------------

* Fix bug related to default urlconf value. 

0.2.0 (2017-04-26)
~~~~~~~~~~~~~~~~~~

* Added ``Step.urlconf`` attribute.
  Allows to use other urlconfigs for running test step.
* Added ``Step.content_type`` attribute.
  Allows to specify custom content types while submitting requests.
* Added ``Step.override_settings`` attribute.
  Allows to override Django settings while making a request.
* Fixed some typos in docstrings.

0.1.0 (2017-03-22)
~~~~~~~~~~~~~~~~~~

* First release on PyPI.


Credits
-------

Development Lead
~~~~~~~~~~~~~~~~

* Miroslav Shubernetskiy  - https://github.com/miki725

Contributors
~~~~~~~~~~~~
* Milind Shakya  - https://github.com/milin 


License
-------

The MIT License (MIT)

Copyright, Dealertrack Technologies, Inc.

::

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.


