###############
release-creator
###############

.. raw:: html

   <img class="brand-wordmark brand-wordmark-light" src="_static/wordmark-light.png" alt="release-creator logo">
   <img class="brand-wordmark brand-wordmark-dark" src="_static/wordmark-dark.png" alt="release-creator logo">

``release-creator`` links named changelog fragments to squash pull requests, validates release tags, and renders
GitHub Release notes from the tagged changelog. Install a published version with
``uvx --from release-creator release-creator``.

The three commands run at different points in a release:

.. list-table:: Choose a command
   :header-rows: 1

   * - Command
     - When to run it
     - Result
   * - :doc:`fragments <how-to/link-fragments>`
     - After squash merge, before Towncrier builds the changelog
     - Adds the pull request link to each named fragment
   * - :doc:`tags <how-to/select-release-tag>`
     - Before preparing a release, then when making the comparison link
     - Checks the version or prints its predecessor
   * - :doc:`notes <how-to/render-notes>`
     - After the changelog and tag exist
     - Prints the GitHub Release body from the tagged changelog

Start with the tutorial for a complete release. Use the how-to guides for an existing project. The reference lists
flags and input formats; the explanation covers the source of each part of a GitHub Release.

The :doc:`changelog <changelog>` includes an ``Unreleased`` section in PR builds when that branch has fragments.
``CHANGELOG.md`` receives those entries when the release is prepared.

.. toctree::
   :caption: Tutorial
   :hidden:

   tutorial/first-release

.. toctree::
   :caption: How-to guides
   :hidden:

   how-to/link-fragments
   how-to/render-notes
   how-to/select-release-tag

.. toctree::
   :caption: Reference
   :hidden:

   reference/cli
   reference/formats

.. toctree::
   :caption: Explanation
   :hidden:

   explanation/release-data

.. toctree::
   :caption: Project
   :hidden:

   changelog
