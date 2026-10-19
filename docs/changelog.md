# Changelog

<!-- towncrier release notes start -->

<a name="release-0-2-0"></a>

## 0.2.0 (2026-10-19)

<a name="release-0-2-0-added"></a>

### Added

- Resolve merged pull request authors for changelog credits and verify them against generated GitHub release notes
  ([#7](https://github.com/tox-dev/release-creator/pull/7)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-2-0-documentation"></a>

### Documentation

- Document the feature-release policy for Python support changes
  ([#5](https://github.com/tox-dev/release-creator/pull/5)) by [@gaborbernat](https://github.com/gaborbernat). Additions
  and drops use feature fragments and select minor releases. New releases will not install on a dropped Python version;
  users who need that version can install an older release.

<a name="release-0-1-1"></a>

## 0.1.1 (2026-10-19)

<a name="release-0-1-1-fixed"></a>

### Fixed

- Keep verified new-contributor credits when GitHub links the contributor's first pull request with a URL
  ([#4](https://github.com/tox-dev/release-creator/pull/4)).

<a name="release-0-1-0"></a>

## 0.1.0 (2026-10-19)

<a name="release-0-1-0-added"></a>

### Added

- Add post-merge pull request links to named changelog fragments, allowing contributors to write entries before a PR
  number exists ([#1](https://github.com/tox-dev/release-creator/pull/1)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Calculate release versions from pending changelog fragments, with explicit bump and CalVer choices
  ([#3](https://github.com/tox-dev/release-creator/pull/3)) by [@gaborbernat](https://github.com/gaborbernat).
- Provide a Towncrier template for Markdown changelogs with stable release and category anchors
  ([#1](https://github.com/tox-dev/release-creator/pull/1)) by [@gaborbernat](https://github.com/gaborbernat).
- Render GitHub Release notes from tagged Markdown and reStructuredText changelogs with user-facing categories, human
  mentions, contributor credits, and comparison links ([#1](https://github.com/tox-dev/release-creator/pull/1)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Validate numeric release tags and select the previous tag for GitHub comparison links
  ([#1](https://github.com/tox-dev/release-creator/pull/1)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-1-0-fixed"></a>

### Fixed

- Format the assembled changelog before release validation so added pull request links and author credits pass `prek`
  ([#2](https://github.com/tox-dev/release-creator/pull/2)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-1-0-documentation"></a>

### Documentation

- Document the release flow with a tutorial, command guides, input formats, and a draft changelog in PR documentation
  builds ([#1](https://github.com/tox-dev/release-creator/pull/1)) by [@gaborbernat](https://github.com/gaborbernat).
