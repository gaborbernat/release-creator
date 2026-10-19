#################
Input formats
#################

Fragments
=========

The fragment linker accepts filenames such as ``+short-name.feature.md``. With ``--git`` it reads each fragment's
introducing squash commit. With ``--commit-map`` it reads a UTF-8 TSV with one fragment filename and one subject per
line. A subject ends with ``(#number)``. The default fragment directory is ``changelog.d``.

The package ships a Towncrier template. After installing release-creator, use it in ``[tool.towncrier]``:

.. code-block:: toml

   template = "release_creator.fragments:template.jinja2"

Towncrier still requires category definitions in the project's ``pyproject.toml``.

Changelog sections
==================

Markdown versions use ``## 1.2.3 (date)`` with level-three category headings. RST versions use ``1.2.3 (date)`` and
category headings with underlines. Empty categories are omitted.

.. list-table:: Category names
   :header-rows: 1

   * - Changelog
     - GitHub Release
   * - Added
     - Features
   * - Changes
     - Changes
   * - Fixed
     - Bug fixes
   * - Documentation
     - Documentation
   * - Breaking changes
     - Breaking changes
   * - Security
     - Security
   * - Performance
     - Performance
   * - Deprecated
     - Deprecations
   * - Removed
     - Removals
   * - Packaging
     - Packaging

GitHub output uses level-three headings and stable ``release-<version>-<category>`` anchors. Each entry may credit
one or more people with linked ``@handle`` text in the changelog; GitHub uses mentions. Bot authors are not credits.
