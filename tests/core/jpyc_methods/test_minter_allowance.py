import pytest

from packages.core.jpyc_core_sdk.utils.errors import (
    InvalidChecksumAddress,
)

from ..conftest import KNOWN_ACCOUNTS


@pytest.mark.parametrize(
    [
        "mocked_eth_contract_functions",
    ],
    [
        pytest.param(
            {
                "func_name": "minterAllowance",
                "func_args": [KNOWN_ACCOUNTS[0].address],
                "return_value": 1000000000000000000000,
            },
        ),
    ],
    indirect=[
        "mocked_eth_contract_functions",
    ],
)
def test_minter_allowance(
    jpyc_client,
    mocked_eth_contract_functions,
):
    minter = KNOWN_ACCOUNTS[0].address

    jpyc_client.minter_allowance(minter=minter)

    mocked_eth_contract_functions.assert_called_once_with(minter)


def test_minter_allowance_failures(
    jpyc_client,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.minter_allowance(minter="invalid_address")
