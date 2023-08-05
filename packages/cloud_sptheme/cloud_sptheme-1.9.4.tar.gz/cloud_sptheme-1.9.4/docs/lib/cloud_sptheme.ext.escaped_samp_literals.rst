==================================================================================================
:mod:`cloud_sptheme.ext.escaped_samp_literals` - permits escaped bracket characters in *samp* role
==================================================================================================

.. module:: cloud_sptheme.ext.escaped_samp_literals
    :synopsis: support escaped bracket characters in SAMP role

Overview
========
This extension modifies how ``:samp:`` literals are parsed, replacing
the default Sphinx parser with an alternate one that allows embedding
literal ``{`` and ``}`` characters within the content, as well providing
stricter input validation.

To embed a literal ``{``, just use a double-backslash, e.g::

    :samp:`this is a {variable}, these are a literal \\{ and \\}`

... and it will be rendered as:

    :samp:`this is a {variable}, these are a literal \\{ and \\}`

Internals
=========
.. rst-class:: float-center

.. seealso::

    This feature has been submitted to Sphinx as
    `issue 789 <https://github.com/sphinx-doc/sphinx/issues/789>`_.
    If/when that issue is resolved, this extension will be deprecated and removed.
