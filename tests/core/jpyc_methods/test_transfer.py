import pytest

from packages.core.jpyc_core_sdk.utils.errors import (
    AccountNotInitialized,
    InvalidChecksumAddress,
    InvalidUint256,
)

from ..conftest import KNOWN_ACCOUNTS


@pytest.mark.parametrize(
    ["mocked_eth_contract_functions"],
    [
        pytest.param(
            {"func_name": "transfer"},
        ),
    ],
    indirect=["mocked_eth_contract_functions"],
)
def test_transfer(
    jpyc_client,
    mocked_eth_contract_functions,
):
    to = KNOWN_ACCOUNTS[1].address
    value = 10000

    jpyc_client.transfer(
        to=to,
        value=value,
    )

    mocked_eth_contract_functions.call_count == 2
    mocked_eth_contract_functions.assert_called_with(
        to=to,
        value=value * 10**18,
    )


@pytest.mark.parametrize(
    [
        "to",
        "value",
        "exception_class",
    ],
    [
        pytest.param(
            "invalid_address",
            10000,
            InvalidChecksumAddress,
            id="invalid to",
        ),
        pytest.param(
            KNOWN_ACCOUNTS[1].address,
            -1,
            InvalidUint256,
            id="invalid value",
        ),
    ],
)
def test_transfer_failures(
    jpyc_client,
    to,
    value,
    exception_class,
):
    with pytest.raises(exception_class):
        jpyc_client.transfer(
            to=to,
            value=value,
        )


def test_transfer_account_not_initialized(
    jpyc_client_without_account,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.transfer(
            to=KNOWN_ACCOUNTS[1].address,
            value=1000,
        )
