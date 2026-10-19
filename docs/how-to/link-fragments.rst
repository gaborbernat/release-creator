################################
Link named fragments after merge
################################

Use named fragments when contributors should be able to write release notes before a pull request number exists. The
``fragments`` command reads each file's introducing squash commit from Git. Each subject must end in ``(#number)``. It
inserts the corresponding GitHub pull request link in the fragment text.

.. code-block:: bash

   uvx --from release-creator==0.1.0 release-creator fragments --directory changelog.d --repository owner/project --git

Run this command before ``towncrier build``, because Towncrier removes consumed fragments. A rerun fails on an already
linked fragment, so it cannot add a duplicate. If Git history is unavailable, supply a tab-separated map of fragment
filenames and squash commit subjects with ``--commit-map commits.tsv``.

For projects that already use numbered fragments, leave their names in place. The linker only needs a map for named
fragments it processes.
