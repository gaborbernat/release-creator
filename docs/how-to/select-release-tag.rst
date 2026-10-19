############################
Select a numeric release tag
############################

Use ``tags`` before preparing a release to reject a version that is not newer than the existing numeric tags. Pass
the Git tags on standard input so the command can ignore other tag formats and compare the numeric components.

.. code-block:: bash

   git tag --list | uvx --from release-creator==0.1.0 release-creator tags 1.2.3 --require-newer

After publishing, use the same input to find the previous release for the GitHub comparison link. An empty result
means this is the first numeric release.

.. code-block:: bash

   git tag --list | uvx --from release-creator==0.1.0 release-creator tags 1.2.3 --previous

Without either option, ``tags`` validates the major.minor.patch format without reading standard input.
