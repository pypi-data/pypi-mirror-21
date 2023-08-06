=======
mdorrst
=======


.. image:: https://img.shields.io/pypi/v/mdorrst.svg
        :target: https://pypi.python.org/pypi/mdorrst

.. image:: https://img.shields.io/travis/JulienPalard/mdorrst.svg
        :target: https://travis-ci.org/JulienPalard/mdorrst

Tell appart Markdown and reStructuredText.


* Free software: MIT license

Usage
-----

The package exposes a single function, ``sniff(content)``, trying to
deduce the format used, returning it as a string: ``md``, ``rst`` or
``txt``::

  >>> import mdorrst
  >>> mdorrst.sniff("[hey](http://example.com)")
  'md'
  >>> mdorrst.sniff("`hey <http://example.com>`__")
  'rst'


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.4.0 (2017-04-27)
------------------

* Simplify API.


0.3.0 (2017-04-26)
------------------

* Python 2.7 support.


0.2.0 (2017-04-26)
------------------

* Expose ``from_text()``.


0.1.0 (2017-04-26)
------------------

* First release on PyPI.


