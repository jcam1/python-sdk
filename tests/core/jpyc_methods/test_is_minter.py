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
            {"func_name": "isMinter"},
        ),
    ],
    indirect=[
        "mocked_eth_contract_functions",
    ],
)
def test_is_minter(
    jpyc_client,
    mocked_eth_contract_functions,
):
    account = KNOWN_ACCOUNTS[0].address

    jpyc_client.is_minter(account=account)

    mocked_eth_contract_functions.assert_called_once_with(account)


def test_is_minter_failures(
    jpyc_client,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.is_minter(account="invalid_address")
