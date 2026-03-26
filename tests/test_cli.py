from __future__ import annotations

import pytest

from mahjonggstats.cli import validate_sort_option


@pytest.mark.parametrize(
    "sort_opt,expect_error",
    [
        ("", False),
        ("GA", False),
        ("GD", False),
        ("NA", False),
        ("ND", False),
        ("AA", False),
        ("AD", False),
        ("G", False),
        ("N", False),
        ("A", False),
        ("nA", False),
        ("na", False),
        ("Y", True),
        ("XA", True),
        ("GU", True),
        ("ABC", True),
    ],
)
def test_validate_sort_option(sort_opt: str, expect_error: bool) -> None:
    if expect_error:
        with pytest.raises(ValueError):
            validate_sort_option(sort_opt)
    else:
        validate_sort_option(sort_opt)
