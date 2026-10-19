###########################
Render GitHub Release notes
###########################

Pass the changelog from the tagged source. ``notes`` selects exactly one matching version section, converts category
headings to the GitHub names, and keeps list items on one line. An ``.rst`` suffix selects the reStructuredText reader.

.. code-block:: console

   uvx --from release-creator==0.1.0 release-creator notes --changelog docs/changelog.rst --tag 1.2.3 --repository owner/project --previous 1.2.2 --issue-role pull --artifact-url https://pypi.org/project/project/1.2.3/ > release-notes.md

Use ``--issue-role pull`` only when the project's ``:issue:`` links mean pull requests. ``:pr:`` and ``:pull:`` always
link to pull requests. Omit ``--artifact-url`` when there is no separately published artifact; change the link text
with ``--artifact-label`` for ecosystems other than PyPI.

To retain GitHub's ``New Contributors`` section, save the response body's text from the generate-notes API and pass
its path with ``--generated-notes``. Only people also credited in the tagged changelog are retained. The rest of the
generated text, including its banner, is discarded.
