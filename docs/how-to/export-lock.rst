##########################
Export a full project lock
##########################

``locks`` writes a PEP 751 ``pylock.toml`` from uv's project resolution. Use it when release tooling must be pinned
without losing the project's other dependency groups, extras, or supported Python versions. The command runs
``uv lock`` and then exports the runtime dependencies, each group, and each extra separately. It retains uv's
Python and platform markers in the resulting file.

Run it from the project root:

.. code-block:: bash

   uvx --from release-creator release-creator locks
   uv pip sync --preview-features pylock --python .venv/bin/python --group release pylock.toml

The output contains a ``project-runtime`` group for the package's runtime dependencies, every group from
``[dependency-groups]``, and every extra from ``[project.optional-dependencies]``. No group is selected by default.
The command above installs only ``release``. Select ``project-runtime`` when you need the package's runtime
dependencies, or combine it with another group or extra when that environment needs both.

The command updates an existing ``uv.lock``. If none exists, it uses a temporary one and removes it after export.
Commit ``pylock.toml``. Keep ``uv.lock`` untracked unless the project also uses that lock for its own build. A failed
uv resolution leaves the previous ``pylock.toml`` intact and prints uv's error. For a library that supports Python
3.11 but uses Sphinx 9 in its ``docs`` group, declare that group's Python minimum under
``[tool.uv.dependency-groups]``. uv cannot infer that the group is optional from the library's runtime
``requires-python`` alone.

The command reads ``[project].requires-python``. For a tool-only ``pyproject.toml`` without ``[project]``, pass
``--tool-python '>=3.15'`` to describe its release-tool environment. It reserves the ``project-runtime`` group
name for the lock's runtime selection.

At a uv workspace root, the command includes every listed member and combines their groups and extras. Members
must declare the same ``requires-python`` range; a mismatch fails before writing a lock. The root can omit
``[project]`` when its members provide that range.
