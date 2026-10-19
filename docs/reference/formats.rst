#################
Input formats
#################

Fragments
=========

The fragment linker accepts filenames such as ``+short-name.feature.md``. With ``--git`` it reads each fragment's
introducing squash commit. With ``--commit-map`` it reads a UTF-8 TSV with one fragment filename and one subject per
line. A subject ends with ``(#number)``. The default fragment directory is ``changelog.d``. The package ships its
Towncrier template; projects can set
``template = "release_creator.fragments:template.jinja2"`` in ``[tool.towncrier]`` after installing release-creator.
Towncrier still requires category definitions in the project's ``pyproject.toml``.

Changelog sections
==================

Markdown versions use ``## 1.2.3 (date)`` and categories use ``### Added``, ``### Changes``, ``### Fixed``,
``### Documentation``, ``### Breaking changes``, ``### Security``, ``### Performance``, ``### Deprecated``,
``### Removed``, or ``### Packaging``. RST versions use ``1.2.3 (date)`` with an underline and the same category
names with underlines. Empty categories are omitted.

GitHub output changes ``Added`` to ``Features``, ``Fixed`` to ``Bug fixes``, ``Deprecated`` to ``Deprecations``, and
``Removed`` to ``Removals``. It uses level-three headings and stable ``release-<version>-<category>`` anchors. The
other category names carry through. Each entry may credit one or more people with linked ``@handle`` text in the
changelog; GitHub uses mentions. Bot authors are not credits.
