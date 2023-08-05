====================================================
Django Active View: *Highlight active items in menu*
====================================================

.. image:: https://img.shields.io/pypi/v/django-activeview.svg
    :target: https://pypi.python.org/pypi/django-activeview
    :alt: PyPi

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://pypi.python.org/pypi/django-activeview/
    :alt: MIT

.. image:: https://img.shields.io/travis/illagrenan/django-activeview.svg
    :target: https://travis-ci.org/illagrenan/django-activeview
    :alt: TravisCI

.. image:: https://img.shields.io/coveralls/illagrenan/django-activeview.svg
    :target: https://coveralls.io/github/illagrenan/django-activeview?branch=master
    :alt: Coverage

.. image:: https://pyup.io/repos/github/illagrenan/django-activeview/shield.svg
    :target: https://pyup.io/repos/github/illagrenan/django-activeview/
    :alt: Updates

.. image:: https://img.shields.io/pypi/implementation/django-activeview.svg
    :target: https://pypi.python.org/pypi/django_brotli/
    :alt: Supported Python implementations

.. image:: https://img.shields.io/pypi/pyversions/django-activeview.svg
    :target: https://pypi.python.org/pypi/django_brotli/
    :alt: Supported Python versions

Introduction
------------

Django template tag that checks if given view or path is active.

Installation
------------

- Supported Python versions are: ``2.7``, ``3.4``, ``3.5``, ``3.6`` and ``pypy``.
- Supported Django versions are: ``1.8.x``, ``1.9.x``, ``1.10.x`` and `1.11.x`.

.. code:: shell

    pip install --upgrade django-activeview


Add ``activeview`` to ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = [
        # ...
        'activeview',
        # ...
    ]

Usage
-----

Template tag ``isactive`` accepts name of url OR path.

.. code:: html+django

    {% load activeview %}

    {% isactive "/" %}
        Root path ("/") is active
    {% endisactive %}

    Or:

    {% isactive "index" %}
        Url with name "index" is active
    {% endisactive %}

    Else is supported:

    {% isactive "contact_us" %}
        Url with name "contact_us" is active.
        {% else %}
        "contact_us" is NOT active
    {% endisactive %}




Inspiration and Credits
-----------------------

- https://github.com/j4mie/django-activelink
- http://stackoverflow.com/a/18772289/752142


License
-------

The MIT License (MIT)

Copyright (c) 2016–2017 Vašek Dohnal (@illagrenan)

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
