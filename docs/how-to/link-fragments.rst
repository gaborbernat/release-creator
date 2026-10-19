################################
Link named fragments after merge
################################

``fragments`` answers one question: which merged pull request introduced each named changelog entry? Contributors can
write ``+cache.bugfix.md`` before a pull request number exists. Run the command on the default branch after squash
merge and before Towncrier consumes the fragments.

What the command changes
========================

Given this fragment:

.. code-block:: markdown

   Avoid stale cache reads by [@alice](https://github.com/alice).

and an introducing squash subject of ``Fix stale cache reads (#42)``, run:

.. code-block:: bash

   uvx --from release-creator release-creator fragments \
     --repository owner/project \
     --git

``--git`` reads the subject of the commit that added each named fragment. ``--repository`` supplies the target for
the pull request link. The command edits the fragment in place:

.. code-block:: markdown

   Avoid stale cache reads ([#42](https://github.com/owner/project/pull/42)) by [@alice](https://github.com/alice).

The author credit stays in the fragment and later in the changelog. For a fragment without ``by``, the link goes at
the end of its sentence. Towncrier then copies the linked text into the release section.

Rules and failure cases
=======================

Write one fragment per user-visible change, including multiple changes in one pull request. Maintenance work without
a user-visible change needs no fragment. A bot pull request needs a fragment only when that pull request supplies one.
The command does not decide whether a change is newsworthy; review that before merging.

The linker processes filenames beginning with ``+`` in the fragment directory. It requires the introducing squash
subject to end in ``(#number)`` and rejects a fragment that already has a pull request link for this repository.
Numbered fragments are left alone. A missing Git history, missing pull request marker, or duplicate link stops the
command before Towncrier builds the changelog.

Other input sources
===================

Use ``--directory`` if the fragments are outside ``changelog.d``. If the checkout lacks Git history, supply a UTF-8
tab-separated map of fragment names to squash subjects instead of ``--git``:

.. code-block:: bash

   printf '%s\t%s\n' '+cache.bugfix.md' 'Fix stale cache reads (#42)' > commits.tsv
   uvx --from release-creator release-creator fragments \
     --repository owner/project \
     --commit-map commits.tsv

``--git`` and ``--commit-map`` are alternatives. Use one of them; the command will not guess a pull request number
from the fragment filename or from its text.
