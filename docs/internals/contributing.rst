Contributing to Cassowary
=========================

If you experience problems with Cassowary, `log them on GitHub`_. If you want
to contribute code, please `fork the code`_ and `submit a pull request`_.


.. _log them on Github: https://github.com/brodderickrodriguez/cassowary/issues
.. _fork the code: https://github.com/brodderickrodriguez/cassowary
.. _submit a pull request: https://github.com/brodderickrodriguez/cassowary/pulls


Setting up your development environment
---------------------------------------

The recommended way of setting up your development environment for Cassowary
is to install a virtual environment, install the required dependencies and
start coding. Assuming that you are using ``virtualenvwrapper``, you only have
to run::

    $ git clone https://github.com/brodderickrodriguez/cassowary.git
    $ cd cassowary
    $ mkvirtualenv cassowary

Cassowary uses ``unittest`` (or ``unittest2`` for Python < 2.7) for its own test
suite as well as additional helper modules for testing. If you are running a
Python version ``< 2.7`` you will also need to ``pip install unittest2``.

Now you are ready to start hacking! Have fun!
