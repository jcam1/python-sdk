import pytest

from packages.core.src.utils.errors import (
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
                "func_name": "balanceOf",
                "func_args": [KNOWN_ACCOUNTS[0].address],
                "return_value": 1000000000000000000000,
            },
        ),
    ],
    indirect=[
        "mocked_eth_contract_functions",
    ],
)
def test_balance_of(
    jpyc_client,
    mocked_eth_contract_functions,
):
    account = KNOWN_ACCOUNTS[0].address

    jpyc_client.balance_of(account=account)

    mocked_eth_contract_functions.assert_called_once_with(account)


def test_balance_of_failures(
    jpyc_client,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.balance_of(account="invalid_address")
