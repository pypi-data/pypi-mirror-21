.. index:: cloud; feature test

============
Feature Test
============

This page contains examples of various features of the Cloud theme.
It's mainly useful internally, to make sure everything is displaying correctly.

Inline Text
=============

Inline literal: ``literal text``.

Samp literal: :samp:`this is a {variable}, these are literal \\{ and \\}`.

External links are prefixed with an arrow: `<http://www.google.com>`_.

But email links are not prefixed: bob@example.com.

Issue tracker link: :issue:`5`.

.. role:: strike
    :class: strike

This text should be :strike:`crossed out`

.. rst-class:: hidden

This text should not be visible.

Admonition Styles
=================
.. note::
    This is a note.

.. caution::

    This is a slightly dangerous.

.. warning::

    This is a warning.

.. danger::

    This is dangerous.

.. seealso::

    This is a "see also" message.

.. todo::

    This is a todo message.

    With some additional next on another line.

.. deprecated:: XXX This is a deprecation warning.

.. versionadded:: XXX This was added

.. versionchanged:: XXX This was changed

.. rst-class:: float-right

.. note::

    This is note using the ``float-right`` class.

.. rst-class:: float-center

.. note::

    This is note using the ``float-center`` class.

.. rst-class:: without-title

.. seealso::
    This is a "see also" using the ``without-title`` class.

Code Styles
===========
Python Code Block:

.. code-block:: python
    :linenos:

    >>> import os

    >>> os.listdir("/home")
    ['bread', 'pudding']

    >>> os.listdir("/root")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    OSError: [Errno 13] Permission denied: '/root'

INI Code Block:

.. code-block:: ini
    :linenos:

    [rueben]
    bread = rye
    meat = corned beef
    veg = sauerkraut

Long Lines (:issue:`22`):

.. literalinclude:: _static/longline.txt
   :linenos:

.. literalinclude:: _static/longline.txt


Function styling:

.. function:: frobfunc(foo=1, *, bar=False)

    :param foo: foobinate strength
    :type foo: int

    :param bar: enabled barring.
    :type bar: bool

    :returns: frobbed return
    :rtype: str

    :raises TypeError: if *foo* is out of range

Class styling:

.. class:: FrobClass(foo=1, *, bar=False)

    Class docstring. Saying things.

    .. attribute:: foo

        foobinate strength

    .. attribute:: bar

        barring enabled

    .. method:: run()

        execute action, return result.

Table Styles
============

.. table:: Normal Table

    =========== =========== ===========
    Header1     Header2     Header3
    =========== =========== ===========
    Row 1       Row 1       Row 1
    Row 2       Row 2       Row 2
    Row 3       Row 3       Row 3
    =========== =========== ===========

.. rst-class:: plain

.. table:: Plain Table (no row shading)

    =========== =========== ===========
    Header1     Header2     Header3
    =========== =========== ===========
    Row 1       Row 1       Row 1
    Row 2       Row 2       Row 2
    Row 3       Row 3       Row 3
    =========== =========== ===========

.. rst-class:: centered

.. table:: Centered Table

    =========== =========== ===========
    Header1     Header2     Header3
    =========== =========== ===========
    Row 1       Row 1       Row 1
    Row 2       Row 2       Row 2
    Row 3       Row 3       Row 3
    =========== =========== ===========

.. rst-class:: fullwidth

.. table:: Full Width Table

    =========== =========== ===========
    Header1     Header2     Header3
    =========== =========== ===========
    Row 1       Row 1       Row 1
    Row 2       Row 2       Row 2
    Row 3       Row 3       Row 3
    =========== =========== ===========

.. table:: :doc:`Table Styling Extension <lib/cloud_sptheme.ext.table_styling>`
    :widths: 1 2 3
    :header-columns: 1
    :column-alignment: left center right
    :column-dividers: none single double single
    :column-wrapping: nnn

    =========== =========== ===========
    Width x1    Width x2    Width x3
    =========== =========== ===========
    Header 1    Center 1    Right 1
    Header 2    Center 2    Right 2
    Header 3    Center 3    Right 3
    =========== =========== ===========

.. table:: :doc:`Table Styling Extension <lib/cloud_sptheme.ext.table_styling>` -- header alignment & colspans
    :widths: 1 1 1 1 2 2 4 4
    :header-alignment: lrlrlrlr
    :column-alignment: lccccccc
    :column-wrapping: tttttttt
    :column-dividers: 122222221

    ======== ======== ======== ======== ======== ======== ================= =================
    Left x1  Right x1 Left x1  Right x1 Left x2  Right x2 Left x4           Right x4
    ======== ======== ======== ======== ======== ======== ================= =================
    Left Span x1+1    Center Span x1+1+2+2                Center Span x4+4
    ----------------- ----------------------------------- -----------------------------------
    Center Span xALL
    -----------------------------------------------------------------------------------------
    Center Span xALL
    =========================================================================================

.. table:: :doc:`Table Styling Extension <lib/cloud_sptheme.ext.table_styling>` -- multi-row header + header columns
    :widths: 1 1 1 1 2 2 4 4
    :header-alignment: lrlrlrlr
    :column-alignment: lccccccc
    :column-wrapping: tttttttt
    :column-dividers: 122222221
    :header-columns: 1

    ======== ======== ======== ======== ======== ======== ================= =================
    Left x1  Right x1 Left x1  Right x1 Left x2  Right x2 Left x4           Right x4
    -------- -------- -------- -------- -------- -------- ----------------- -----------------
    Left Span x1+1    Center Span x1+1+2+2                Center Span x4+4
    ================= =================================== ===================================
    H x1     x1       Center Span x1+1  Center Span x2+2  Center Span x4+4
    -------- -------- ----------------- ----------------- -----------------------------------
    H x1     Center Span xALL
    ======== ================================================================================

.. rst-class:: html-toggle

.. _toggle-test-link:

Toggleable Section
==================
This section is collapsed by default.
But if a visitor follows a link to this section or something within it
(such as :ref:`this <toggle-test-link>`), it will automatically be expanded.

.. rst-class:: html-toggle expanded

Toggleable Subsection
---------------------
Subsections can also be marked as toggleable.
This one should be expanded by default.

Normal Section
==============

Child Section
-------------

.. rst-class:: html-toggle

Toggleable Subsection
---------------------
Test of emphasized + toggleable styles. Should be collapsed by default.

.. rst-class:: emphasize-children

Section With Emphasized Children
================================
Mainly useful for sections with many long subsections,
where a second level of visual dividers would be useful.

Child Section
----------------
Should have slightly lighter background, and be indented.

.. rst-class:: html-toggle

Toggleable Subsection
---------------------
Test of emphasized + toggleable styles. Should be collapsed by default.

:mod:`~cloud_sptheme.ext.autodoc_sections` Extension
====================================================
.. autofunction:: cloud_sptheme.ext.autodoc_sections._doctestfunc
