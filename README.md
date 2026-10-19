# release-creator

Release preparation tools shared by tox-dev projects. The first command renders a tagged changelog section for a GitHub
Release. Later commands can cover other release tasks without changing the `notes` interface.

## Render GitHub Release notes

Use a pinned Git commit until the package is on PyPI:

```bash
uvx --from 'git+https://github.com/tox-dev/release-creator@<commit>' release-creator notes \
  --changelog CHANGELOG.md \
  --tag 1.2.3 \
  --repository tox-dev/example \
  --previous 1.2.2 \
  --artifact-url https://pypi.org/project/example/1.2.3/ > release-notes.md
```

The command reads the tagged section, maps `Added` to `Features` and `Fixed` to `Bug fixes`, changes linked author
handles to GitHub mentions, and leaves bullets unwrapped. It keeps stable category anchors, omits empty categories when
they are absent from the source, and adds artifact and comparison links. Use `--artifact-label` for an ecosystem other
than PyPI; omit `--artifact-url` when there is no external artifact.

The changelog is the source of truth. The command does not infer changes from commits or generate an author list. Add
verified human credits to changelog entries before release; omit bot credits. The GitHub Release may add a
`New Contributors` section separately when GitHub history establishes one.

## Development and releases

See [contributing](CONTRIBUTING.md) for the fragment format and release process. The package uses the same `notes`
command for its own GitHub Releases. Run `tox -e 3.15,type,pkg_meta` and `prek run --all-files` before a PR.
