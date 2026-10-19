##################
Your first release
##################

This tutorial takes a project with a Towncrier changelog from one named fragment to a GitHub Release body. It assumes
the project uses squash merges and has an existing ``[tool.towncrier]`` configuration.

.. mermaid::
   :alt: A named fragment passes through a squash merge, pull request linking, and Towncrier before becoming GitHub Release notes.
   :caption: The release path
   :align: center

   flowchart LR
      fragment["Named fragment"] --> link["Squash merge + PR link"]
      link --> changelog["Tagged changelog"]
      changelog --> notes["GitHub notes"]
      classDef source fill:#dbeafe,stroke:#2563eb,color:#0f172a;
      classDef step fill:#ede9fe,stroke:#7c3aed,color:#0f172a;
      classDef result fill:#dcfce7,stroke:#16a34a,color:#0f172a;
      class fragment source;
      class link step;
      class changelog,notes result;

1. Add ``changelog.d/+cache.bugfix.md`` to the pull request:

   .. code-block:: text

      Avoid stale cache reads by [@alice](https://github.com/alice).

   The filename can be chosen before a pull request number exists. Add one fragment per user-visible change.

2. After squash merging pull request 42, write the fragment name and squash subject to ``commits.tsv``. Separate them
   with a tab:

   .. code-block:: text

      +cache.bugfix.md	Fix stale cache reads (#42)

   Run the linker before Towncrier consumes the fragments:

   .. code-block:: bash

      uvx --from release-creator==0.1.0 release-creator fragments --repository owner/project --commit-map commits.tsv

   The fragment now ends with a link to pull request 42. The command rejects a subject without ``(#42)``.

3. Build the changelog with the project's Towncrier setup:

   .. code-block:: bash

      uvx --from towncrier --with release-creator==0.1.0 towncrier build --version 1.2.3 --yes

   Check that ``CHANGELOG.md`` has a ``## 1.2.3 (...)`` section and a ``### Fixed`` section. The fragment text and
   linked author remain in the changelog.

4. Render the GitHub Release body from that tagged source:

   .. code-block:: bash

      uvx --from release-creator==0.1.0 release-creator notes --changelog CHANGELOG.md --tag 1.2.3 --repository owner/project --previous 1.2.2 --artifact-url https://pypi.org/project/project/1.2.3/ > release-notes.md

   The body uses ``### Bug fixes``, mentions ``@alice``, links to PyPI, and ends with the comparison between 1.2.2
   and 1.2.3. Review ``release-notes.md`` before using it with ``gh release create --notes-file``.
