===============================
TopShape
===============================


.. image:: https://img.shields.io/pypi/v/topshape.svg
        :target: https://pypi.python.org/pypi/topshape

.. image:: https://img.shields.io/travis/mchlumsky/topshape.svg
        :target: https://travis-ci.org/mchlumsky/topshape

.. image:: https://readthedocs.org/projects/topshape/badge/?version=latest
        :target: https://topshape.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/mchlumsky/topshape/shield.svg
        :target: https://pyup.io/repos/github/mchlumsky/topshape/
        :alt: Updates

.. image:: https://pyup.io/repos/github/mchlumsky/topshape/python-3-shield.svg
        :target: https://pyup.io/repos/github/mchlumsky/topshape/
        :alt: Python 3

.. image:: https://codecov.io/gh/mchlumsky/topshape/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/mchlumsky/topshape


Library for easily creating text interfaces that look like Linux's top program.

It is built on top of urwid_ but requires no knowledge of urwid itself.

.. _urwid: http://urwid.org/

* Free software: MIT license
* Documentation: https://topshape.readthedocs.io.
* Python versions supported: 2.7, 3.3, 3.4, 3.5, 3.6

**********
Quickstart
**********

Here's an example of how to use TopShape:

.. code:: python

    from topshape import TopShape


    # The columns are a list (or tuple) of dictionaries. Each
    # dictionary defines a column in the body
    columns = ({'label': 'header1'},
               {'label': 'header2'},
               {'label': 'header3'})


    # The body function will be passed as a callback that must
    # return a 2-dimensional array everytime it's called.
    def body():
        return [[str(i*j) for i in range(3)] for j in range(10)]


    # The header function will be passed as a callback that must
    # return a string everytime it's called.
    def header():
        return 'This is the header!'


    # The footer function will be passed as a callback that must
    # return a string everytime it's called.
    def footer():
        return 'This is the footer!'


    def handle_q(app):
        app.exit()

    def handle_f(app, answer):
        # do something with the answer
        # ...

    # key_map maps keys pressed to callbacks
    key_map = {'q': handle_q,
               'f': (handle_f, 'Enter some text here:'}

    app = TopShape.create_app(columns, body, header, footer,
                              key_mapping=key_map)
    app.run()


Output:

.. image:: https://raw.githubusercontent.com/mchlumsky/topshape/master/docs/example1.png

Output (waiting for input from user):

.. image:: https://raw.githubusercontent.com/mchlumsky/topshape/master/docs/example1-1.png

There is also a more complete example here_ which is a clone of the linux top program.

.. _here: https://github.com/mchlumsky/topshape/blob/master/bin/toppy

Screenshot:

.. image:: https://raw.githubusercontent.com/mchlumsky/topshape/master/docs/example2.png


*******
Credits
*******

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

