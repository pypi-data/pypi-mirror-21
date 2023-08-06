MarkdownMail
============

Purpose
-------

Send e-mails with generated html content.

The content has to be written in Markdown syntax. The text part of the e-mail
will be filled verbatim; the html part will be a converted HTML from the
Markdown content.

Install
-------

``$ pip install markdownmail``


Basic Usage
-----------

.. code:: python

    import markdownmail

    CONTENT = u"""
    SPAMS AND EGGS
    ==============

    This is a demo with a list:

    1. Spam
    2. Second spam
    3. ...and eggs
    """

    email = markdownmail.MarkdownMail(
        from_addr=(u'alice@example.com', u'Alice'),
        to_addr=(u'bob@example.com', u'Bob'),
        subject=u'MarkdownMail demo',
        content=CONTENT
    )

    email.send('localhost')


Content must be unicode.


Run tests
---------

Tox is automatically installed in virtualenvs before executing the tests.
Execute them with:

``$ python setup.py test``


Disable markdownmail in your tests
----------------------------------

If an instance of NullServer is passed to send() method, the e-mail is not send:

.. code:: python

    email = markdownmail.MarkdownMail(
        #params
    )

    email.send(markdownmail.NullServer())


Subclassing NullServer allows to provide a custom behaviour for the send()
method.


Useful links
------------

Envelopes library: https://pypi.python.org/pypi/Envelopes/0.4

Markdown syntax: https://daringfireball.net/projects/markdown/syntax




