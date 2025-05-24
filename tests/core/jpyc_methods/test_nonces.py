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
                "func_name": "nonces",
            },
        ),
    ],
    indirect=[
        "mocked_eth_contract_functions",
    ],
)
def test_nonces(
    jpyc_client,
    mocked_eth_contract_functions,
):
    owner = KNOWN_ACCOUNTS[0].address

    jpyc_client.nonces(owner=owner)

    mocked_eth_contract_functions.assert_called_once_with(owner)


def test_nonces_failures(
    jpyc_client,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.nonces(owner="invalid_address")
