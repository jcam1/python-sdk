from decimal import Decimal

import pytest

from packages.core.src.utils.currencies import (
    remove_decimals,
    restore_decimals,
)


@pytest.mark.parametrize(
    ["value", "response"],
    [
        pytest.param(
            10000,
            10000000000000000000000,
            id="integer",
        ),
        pytest.param(
            0.05,
            50000000000000000,
            id="decimal",
        ),
    ],
)
def test_remove_decimals(value, response):
    on_chain_value = remove_decimals(value=value)
    assert on_chain_value == response


@pytest.mark.parametrize(
    ["value", "response"],
    [
        pytest.param(
            10000000000000000000000,
            10000,
            id="integer",
        ),
        pytest.param(
            50000000000000000,
            Decimal("0.05"),
            id="decimal",
        ),
    ],
)
def test_restore_decimals(value, response):
    off_chain_value = restore_decimals(func=lambda v: v)(value)
    assert off_chain_value == response
