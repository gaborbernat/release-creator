"""Numeric release tag selection tests."""

import pytest

lazy from release_creator.tags.select import parse_tag, previous_tag, require_newer_tag


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        pytest.param("1.2.3", (1, 2, 3), id="normal"),
        pytest.param("01.002.3", (1, 2, 3), id="leading-zeros"),
    ],
)
def test_parse_tag(tag: str, expected: tuple[int, int, int]) -> None:
    assert parse_tag(tag) == expected


@pytest.mark.parametrize(
    "tag",
    [
        pytest.param("1.2", id="short"),
        pytest.param("1.2.3.4", id="long"),
        pytest.param("1.2.", id="empty"),
        pytest.param("1.2.x", id="non-numeric"),
        pytest.param("\u0661.2.3", id="non-ascii"),
    ],
)
def test_parse_tag_rejects_invalid(tag: str) -> None:
    with pytest.raises(ValueError, match=r"(?x)expected\ a\ major\.minor\.patch\ version # Invalid tag format"):
        parse_tag(tag)


def test_previous_tag_uses_numeric_order() -> None:
    assert previous_tag("1.10.0", ["1.9.0", "1.2.0", "junk", "1.10.0", "2.0.0"]) == "1.9.0"


def test_previous_tag_missing() -> None:
    assert previous_tag("1.0.0", ["junk", "1.0.0", "2.0.0"]) is None


def test_require_newer_tag_accepts_first_release() -> None:
    require_newer_tag("1.0.0", ["junk"])


def test_require_newer_tag_accepts_new_version() -> None:
    require_newer_tag("1.10.0", ["junk", "1.9.0"])


@pytest.mark.parametrize(
    "tag",
    [pytest.param("1.9.0", id="same"), pytest.param("1.8.9", id="older")],
)
def test_require_newer_tag_rejects_existing(tag: str) -> None:
    with pytest.raises(ValueError, match="must be newer"):
        require_newer_tag(tag, ["junk", "1.9.0"])
