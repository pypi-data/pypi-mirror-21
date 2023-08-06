..
    :copyright: Copyright (c) 2014 ftrack

*****
Using
*****

Once you have Lowdown :ref:`installed <installing>`, add it as an extension to
your `Sphinx configuration file <http://sphinx-doc.org/config.html>`_::

    # conf.py
    extensions = [
        'lowdown'
    ]

Now add relevant :class:`release <lowdown.ReleaseDirective>` and :class:`change
<lowdown.ChangeDirective>` directives to an included source file, such as
:file:`release.rst` to detail each release::

    .. release:: 0.1.0
        :date: 2015-01-01

        .. change:: new
            :tags: interface

            Added a fantastic new feature to the interface that you will all
            love.

        .. change:: fixed
            :changeset: c0381d8
            :tags: api, documentation

            Fixed an embarrisng issue in the API and updated documentation to
            be clearer as well.

        .. change:: changed
            :tags: interface

            That shiny button is now red!
            `Read more <http://en.wikipedia.org/wiki/Parkinson%27s_law_of_triviality>`_

Once built, it will look like:

.. image:: /image/example.png

Configuring
===========

In the configuration file you can also specify Lowdown specific options to
control the output:

.. option:: lowdown_date_format

    The format string to use with :meth:`arrow.get
    <arrow.factory.ArrowFactory.get>` when rendering the release date. Defaults
    to ``D MMMM YYYY``.

.. option:: lowdown_release_link

    Control how release links are generated. Can be either a format string that
    has ``{value}`` in it where the release string should be, or a callable that
    accepts the release string and returns a full URI string. If not specified,
    release titles will be plain text and not links.

.. option:: lowdown_changeset_link

    Control how changeset links are generated. Can be either a format string
    that has ``{value}`` in it where the changeset string should be, or a callable
    that accepts the changeset string and returns a full URI string.

    If not specified, changeset references will be plain text and not links.

Styling
=======

By default, a :file:`lowdown.css` stylesheet is added with some basic styling.
Take a look to see which classes you can use in a custom stylesheet to further
control styling.
