Instagram Scraper
=================

|PyPI| |Build Status|

instagram-scraper is a command-line application written in Python that
scrapes and downloads an instagram user’s photos and videos. Use
responsibly.

Install
-------

To install instagram-scraper:

.. code:: bash

    $ pip install instagram-scraper

Usage
-----

To scrape a public user’s media:

.. code:: bash

    $ instagram-scraper <username>

To specify multiple users, pass a delimited list of users:

.. code:: bash

    $ instagram-scraper username1,username2,username3

You can also supply a file containing a list of usernames:

.. code:: bash

    $ instagram-scraper -f ig_users.txt

::

    # ig_users.txt

    username1
    username2
    username3

    # and so on...

The usernames may be separated by newlines, commas, semicolons, or
whitespace.

To specify the download destination:

.. code:: bash

    $ instagram-scraper <username> -d /path/to/destination

By default, media will be download to
*``<current working directory>/<username>``*

To scrape a private user’s media when you are an approved follower:

.. code:: bash

    $ instagram-scraper <username> -u <your username> -p <your password>

Develop
-------

Clone the repo and create a virtualenv

.. code:: bash

    $ virtualenv venv
    $ source venv/bin/activate
    $ python setup.py develop

Running Tests
-------------

.. code:: bash

    $ python setup.py test

    # or just

    $ nosetests

Contributing
------------

#. Check the open issues or open a new issue to start a discussion
   around
   your feature idea or the bug you found
#. Fork the repository, make your changes, and add yourself to
   `AUTHORS.md`_
#. Send a pull request

License
-------

This is free and unencumbered software released into the public domain.

| Anyone is free to copy, modify, publish, use, compile, sell, or
| distribute this software, either in source code form or as a compiled
| binary, for any purpose, commercial or non-commercial, and by any
| means.

| In jurisdictions that recognize copyright laws, the author or authors
| of this software dedicate any and all copyright interest in the
| software to the public domain. We make this dedication for the benefit
| of the public at large and to the detriment of our heirs and
| successors. We intend this dedication to be an overt act of
| relinquishment in perpetuity of all present and future rights to this
| software under copyright law.

| THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
| EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
| MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
| IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
| OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
| ARISING FROM, OUT OF OR IN CONNECTION WITH

.. _AUTHORS.md: AUTHORS.md

.. |PyPI| image:: https://img.shields.io/pypi/v/nine.svg
   :target: https://pypi.python.org/pypi/instagram-scraper
.. |Build Status| image:: https://travis-ci.org/rarcega/instagram-scraper.svg?branch=master
   :target: https://travis-ci.org/rarcega/instagram-scraper