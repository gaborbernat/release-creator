################################
Link named fragments after merge
################################

Use named fragments when contributors should be able to write release notes before a pull request number exists. The
``fragments`` command reads a tab-separated map of fragment filenames to squash commit subjects. Each subject must end
in ``(#number)``. The command inserts the corresponding GitHub pull request link in the fragment text.

.. code-block:: console

   uvx --from release-creator==0.1.0 release-creator fragments --directory changelog.d --repository owner/project --commit-map commits.tsv

Build the map from the commits that introduced the fragments. Run this command before ``towncrier build``, because
Towncrier removes consumed fragments. A rerun fails on an already linked fragment, so it cannot add a duplicate.

For projects that already use numbered fragments, leave their names in place. The linker only needs a map for named
fragments it processes.
