Custom Sphinx themes for the documentation of `my projects <https://github.com/the-allanc/>`_.

Themes
======
- **yeen**: Slight modification of the `TriAx Corp <http://pythonhosted.org/sphinxjp.themes.trstyle/>`_ theme.

 - Defaults to blue colours and sidebar on the left.
 - Field lists now use the *mainlightcolor* option for the background colour for headers, rather than a hardcoded blue colour.

Usage
=====
To use the theme, specify ``allanc_sphinx[yeen]`` as a dependency, and in your ``conf.py`` file::

    html_theme = 'yeen'


