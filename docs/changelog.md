# Changelog

<!-- towncrier release notes start -->

<a name="release-0-6-0"></a>

## 0.6.0 (2026-10-23)

<a name="release-0-6-0-added"></a>

### Added

- Link named changelog fragments to squash-merged pull requests and verified human authors using Git history and GitHub
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).
- Render reStructuredText changelog entries as Markdown GitHub Release notes while preserving links and author credits
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).
- Return verified PyPI file URLs for trusted-publisher attestation after comparing the complete published release with
  local distributions ([#14](https://github.com/tox-dev/release-creator/pull/14)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-6-0-changes"></a>

### Changes

- Read fragment provenance from Git without `--git` or `--commit-map`; use Nab in place of the removed `locks` and
  `build-constraints` commands ([#14](https://github.com/tox-dev/release-creator/pull/14)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-6-0-fixed"></a>

### Fixed

- Accept canonical prerelease, postrelease and development tags, and use PEP 440 order when selecting previous releases
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).
- Finalize a matching prerelease before applying the next version bump
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).
- Fix pull request lookup for named changelog fragments during release preparation
  ([#16](https://github.com/tox-dev/release-creator/pull/16)) by [@gaborbernat](https://github.com/gaborbernat).
- Preview standard Knope changesets without extra section configuration
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).
- Read Towncrier defaults and validate fragments from project subdirectories
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).
- Reject changelog fragments with the wrong file extension before release
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).
- Reject shallow Git histories when attributing changelog fragments to pull requests
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).
- Skip non-Python hook dependencies when refreshing pre-commit pins
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-6-0-security"></a>

### Security

- Use the final credit in generated GitHub notes when a pull request title contains a forged credit
  ([#14](https://github.com/tox-dev/release-creator/pull/14)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-6-0-packaging"></a>

### Packaging

- Include the MIT license file in wheel metadata ([#14](https://github.com/tox-dev/release-creator/pull/14)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-5-1"></a>

## 0.5.1 (2026-10-22)

<a name="release-0-5-1-fixed"></a>

### Fixed

- Refresh transitive pre-commit hook dependencies alongside direct pins, including platform-specific packages
  ([#13](https://github.com/tox-dev/release-creator/pull/13)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-5-0"></a>

## 0.5.0 (2026-10-22)

<a name="release-0-5-0-added"></a>

### Added

- Add a `hooks` command to refresh exact pre-commit `additional_dependencies` pins under a release-age cutoff without
  rewriting the rest of the hook configuration ([#11](https://github.com/tox-dev/release-creator/pull/11)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Allow repositories whose numeric Towncrier fragment stems are pull request numbers to preserve the original pull
  request link and verified author during historical backfills
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Calculate versions from `v`-prefixed release tags and retain that prefix when requested
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Check PyPI filenames and SHA256 digests before retrying a partial upload, stage only missing files, and verify the
  complete published set afterward ([#11](https://github.com/tox-dev/release-creator/pull/11)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Check a JetBrains Marketplace plugin against its signed ZIP before retrying an upload
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Export one selectable pylock.toml for a project's runtime dependencies, groups, extras, Python range, and platforms
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Include YAML support in the base package so every command works without an extra
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Include build backend dependencies in the full project lock and select exact, hashed build constraints for the current
  Python and platform ([#11](https://github.com/tox-dev/release-creator/pull/11)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Link Knope changesets to merged pull requests and repair changelog anchors after release preparation
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Render package and Knope draft fragments beside released history in documentation builds without changing the tracked
  changelog ([#11](https://github.com/tox-dev/release-creator/pull/11)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Select and validate package-prefixed tags from a mixed repository tag list
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Select hashed build constraints for named operating systems and Python versions, and reject a shared file when their
  dependency selections differ ([#11](https://github.com/tox-dev/release-creator/pull/11)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Validate changed pull request fragments with the Towncrier configuration
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-5-0-fixed"></a>

### Fixed

- Convert Sphinx PEP references to links in GitHub Release notes rendered from reStructuredText changelogs
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Convert reStructuredText links in changelog entries to Markdown links in GitHub Release notes
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Credit the merged pull request author for numeric fragments without losing a separate issue link
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Keep GitHub first-contributor credits for human pull requests without a changelog entry
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Keep explicit display text from reStructuredText links in GitHub Release notes
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Keep first-time human contributor credits when GitHub generated notes use a level-three heading
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Keep wrapped reStructuredText author credits attached to their release entry
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Preserve RST field names inside inline code when rendering GitHub release notes
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Preserve each reStructuredText changelog’s configured category heading level when assembling a release
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Preserve named historical author credits when GitHub generated notes omit a deleted account's handle
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Preserve nested lists, code blocks, and warnings when rendering reStructuredText release notes for GitHub
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Reject named changelog fragments without a `+` prefix before version selection or release assembly
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Render a credited historical pull request when GitHub generated notes omit it
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Render historical RST release headings that link to a tag but have no date
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).
- Render prerelease and four-part historical version sections in GitHub Release notes
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-5-0-documentation"></a>

### Documentation

- Clarify when to keep `uv.lock` alongside the exported `pylock.toml`
  ([#11](https://github.com/tox-dev/release-creator/pull/11)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-4-1"></a>

## 0.4.1 (2026-10-19)

<a name="release-0-4-1-fixed"></a>

### Fixed

- Render historical release notes for two-part version tags such as 0.2
  ([#10](https://github.com/tox-dev/release-creator/pull/10)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-4-0"></a>

## 0.4.0 (2026-10-19)

<a name="release-0-4-0-added"></a>

### Added

- Render older uncategorized release entries under Other changes without assigning a user-facing category to them
  ([#9](https://github.com/tox-dev/release-creator/pull/9)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-3-0"></a>

## 0.3.0 (2026-10-19)

<a name="release-0-3-0-added"></a>

### Added

- Select one package history from a shared Markdown changelog and keep its package-prefixed comparison tags
  ([#8](https://github.com/tox-dev/release-creator/pull/8)) by [@gaborbernat](https://github.com/gaborbernat).
- Ship a reStructuredText Towncrier template with stable anchors that follows each changelog's heading style
  ([#8](https://github.com/tox-dev/release-creator/pull/8)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-3-0-fixed"></a>

### Fixed

- Keep Towncrier's issue links when a release contains numbered fragments alongside named fragments
  ([#8](https://github.com/tox-dev/release-creator/pull/8)) by [@gaborbernat](https://github.com/gaborbernat).
- Read bracketed and v-prefixed Markdown release headings when rendering GitHub Release notes
  ([#8](https://github.com/tox-dev/release-creator/pull/8)) by [@gaborbernat](https://github.com/gaborbernat).
- Reject uncategorized release items and empty category headings before tagging or publishing a distribution
  ([#8](https://github.com/tox-dev/release-creator/pull/8)) by [@gaborbernat](https://github.com/gaborbernat).
- Replace a changelog's existing comparison line when rendering GitHub Release notes, so the body contains one link
  ([#8](https://github.com/tox-dev/release-creator/pull/8)) by [@gaborbernat](https://github.com/gaborbernat).
- Select automatic release versions from reStructuredText fragments as well as Markdown fragments
  ([#8](https://github.com/tox-dev/release-creator/pull/8)) by [@gaborbernat](https://github.com/gaborbernat).

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
