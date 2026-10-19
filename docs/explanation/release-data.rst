#############################
Where release data comes from
#############################

The tagged changelog supplies the release entries, order, categories, and human credits. This keeps the published
description tied to reviewed source rather than to commit subjects. A commit can contain several user-visible changes;
separate fragments preserve those entries. The squash subject supplies only the pull request number for a named
fragment.

.. mermaid::
   :alt: The tagged changelog provides release changes and credited authors; GitHub generated notes contribute only verified first-time contributors to the final GitHub Release body.
   :caption: Sources for a GitHub Release body
   :align: center

   flowchart LR
      changelog["Tagged changelog"] --> render["release-creator notes"]
      changelog -. "Credited authors" .-> filter["Verify contributors"]
      generated["GitHub generated notes"] --> filter
      filter --> render
      render --> release["GitHub Release body"]
      classDef source fill:#dbeafe,stroke:#2563eb,color:#0f172a;
      classDef step fill:#ede9fe,stroke:#7c3aed,color:#0f172a;
      classDef result fill:#dcfce7,stroke:#16a34a,color:#0f172a;
      class changelog,generated source;
      class filter,render step;
      class release result;

GitHub's generated notes can identify first-time contributors, but their change list is not the release description.
When supplied, ``notes`` keeps ``New Contributors`` entries only for handles already credited in the changelog. The
generated banner and categories are not copied.

Towncrier owns fragment collection and changelog assembly. Its package-template setting can use the template shipped
by release-creator. Category definitions still live in each project's configuration. ``release-creator`` handles the
steps Towncrier does not: linking named fragments after squash merge and rendering the final GitHub body.
