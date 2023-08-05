===================================================
:mod:`cloud_sptheme.ext.autoattribute_search_bases`
===================================================

.. module:: cloud_sptheme.ext.autoattribute_search_bases
    :synopsis: make ``autoattribute`` search for docstrings in parent classes

.. versionadded:: 1.7

Overview
========

Currently, :mod:`sphinx.ext.autodoc`'s ``autoattribute`` only checks
the current class for an attribute docstring. This extension patches Sphinx
so that if one isn't found, autodoc will then search through the parent classes,
in case the attribute is defined there, but is being documented in the subclass.
