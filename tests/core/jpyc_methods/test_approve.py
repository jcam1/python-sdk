import pytest

from packages.core.src.utils.errors import (
    AccountNotInitialized,
    InvalidChecksumAddress,
    InvalidUint256,
)

from ..conftest import KNOWN_ACCOUNTS


@pytest.mark.parametrize(
    ["mocked_eth_contract_functions"],
    [
        pytest.param(
            {"func_name": "approve"},
        ),
    ],
    indirect=["mocked_eth_contract_functions"],
)
def test_approve(
    jpyc_client,
    mocked_eth_contract_functions,
):
    spender = KNOWN_ACCOUNTS[1].address
    value = 10000

    jpyc_client.approve(
        spender=spender,
        value=value,
    )

    mocked_eth_contract_functions.call_count == 2
    mocked_eth_contract_functions.assert_called_with(
        spender=spender,
        value=value * 10**18,
    )


@pytest.mark.parametrize(
    [
        "spender",
        "value",
        "exception_class",
    ],
    [
        pytest.param(
            "invalid_address",
            10000,
            InvalidChecksumAddress,
            id="invalid spender",
        ),
        pytest.param(
            KNOWN_ACCOUNTS[1].address,
            -1,
            InvalidUint256,
            id="invalid value",
        ),
    ],
)
def test_approve_failures(
    jpyc_client,
    spender,
    value,
    exception_class,
):
    with pytest.raises(exception_class):
        jpyc_client.approve(
            spender=spender,
            value=value,
        )


def test_approve_account_not_initialized(
    jpyc_client_without_account,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.approve(
            spender=KNOWN_ACCOUNTS[1].address,
            value=1000,
        )
