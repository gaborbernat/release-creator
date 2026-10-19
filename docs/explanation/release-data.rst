#############################
Where release data comes from
#############################

The tagged changelog supplies the release entries, order, categories, and human credits. This keeps the published
description tied to reviewed source rather than to commit subjects. A commit can contain several user-visible changes;
separate fragments preserve those entries. The squash subject supplies only the pull request number for a named
fragment.

GitHub's generated notes can identify first-time contributors, but their change list is not the release description.
When supplied, ``notes`` keeps ``New Contributors`` entries only for handles already credited in the changelog. The
generated banner and categories are not copied.

Towncrier owns fragment collection and changelog assembly. Its package-template setting can use the template shipped
by release-creator. Category definitions still live in each project's configuration. ``release-creator`` handles the
steps Towncrier does not: linking named fragments after squash merge and rendering the final GitHub body.
