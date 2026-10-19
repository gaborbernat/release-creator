############################
Select a numeric release tag
############################

``tags`` makes two decisions for a numeric release: whether the proposed version can follow existing tags, and which
earlier tag belongs in the GitHub comparison link. It reads tag names from standard input. The command never creates
or moves a tag.

Check a proposed version
========================

Suppose ``git tag --list`` prints ``1.2.1``, ``1.2.2``, and ``docs-preview``. Before preparing ``1.2.3``, run:

.. code-block:: bash

   git tag --list | uvx --from release-creator release-creator tags 1.2.3 --require-newer

A successful check prints nothing and exits with status zero. If ``1.2.3`` or a newer numeric tag already exists,
the command fails. This prevents release preparation from reusing a version or publishing an older one. A name such
as ``1.2.3rc1`` also fails: this command accepts exactly three numeric components.

Find the comparison base
========================

For the same tag list, run:

.. code-block:: bash

   git tag --list | uvx --from release-creator release-creator tags 1.2.3 --previous

The output is ``1.2.2``. Pass it to ``notes --previous 1.2.2`` to link the changes since that release. For a first
numeric release, ``--previous`` prints nothing; ``notes`` then links to the commits at the new tag.

Rules and failure cases
=======================

The proposed tag must have ``major.minor.patch`` form. Existing tags with other forms, such as ``docs-preview`` or
``v1.2.2``, do not take part in the comparison. Numeric components are compared as numbers, so ``1.2.10`` follows
``1.2.9``. ``--previous`` selects the greatest numeric tag below the proposed one, regardless of input order.

Without ``--previous`` or ``--require-newer``, the command only validates the proposed tag's format and does not read
standard input. Choose one option at a time; they answer different questions.
