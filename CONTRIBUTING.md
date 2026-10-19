# Contributing to release-creator

Run `tox -e dev` to create `.tox/dev`. Run `tox -e 3.15,type,pkg_meta` and `prek run --all-files` before pushing a PR.
CI also tests Python 3.11–3.15 on Linux, macOS, and Windows.

## Release notes

Add a `changelog.d/<PR>.<type>.md` fragment for each user-visible change. Use `feature` for additions, `change` for
changed behavior, `bugfix` for fixes, or `doc` for documentation. Other types are `breaking`, `security`, `performance`,
`deprecation`, `removal`, and `packaging`. Keep separate changes in separate fragments.

Write a complete sentence, link the PR, and credit verified human authors:

```markdown
Render GitHub notes without wrapped bullets ([#1](https://github.com/tox-dev/release-creator/pull/1)) by [@gaborbernat](https://github.com/gaborbernat).
```

For multiple authors, join linked handles with `by x, y and z`. Do not credit reviewers or bots. Bot PRs need no
fragment unless they supply a user-facing change; a bot-only fragment may omit `by`. Apply `skip news` to maintenance
work. This label may be added after opening the PR, and it does not suppress checks for a supplied fragment.

## Release process

The `Prepare release` workflow assembles a Towncrier changelog patch, runs `prek`, then uses the repository-scoped
release App to commit and tag on `main`. The tag workflow runs `prek` again, builds the package, publishes to PyPI
through trusted publishing, and creates a GitHub Release using the tagged `release-creator` package from GitHub. Set up
the App, `release-auth` environment, and PyPI trusted publisher before dispatching it.
