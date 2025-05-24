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
            {"func_name": "increaseAllowance"},
        ),
    ],
    indirect=["mocked_eth_contract_functions"],
)
def test_increase_allowance(
    jpyc_client,
    mocked_eth_contract_functions,
):
    spender = KNOWN_ACCOUNTS[1].address
    increment = 1000

    jpyc_client.increase_allowance(
        spender=spender,
        increment=increment,
    )

    mocked_eth_contract_functions.call_count == 2
    mocked_eth_contract_functions.assert_called_with(
        spender=spender,
        increment=increment * 10**18,
    )


@pytest.mark.parametrize(
    [
        "spender",
        "increment",
        "exception_class",
    ],
    [
        pytest.param(
            "invalid_address",
            1000,
            InvalidChecksumAddress,
            id="invalid spender",
        ),
        pytest.param(
            KNOWN_ACCOUNTS[1].address,
            -1,
            InvalidUint256,
            id="invalid increment",
        ),
    ],
)
def test_increase_allowance_failures(
    jpyc_client,
    spender,
    increment,
    exception_class,
):
    with pytest.raises(exception_class):
        jpyc_client.increase_allowance(
            spender=spender,
            increment=increment,
        )


def test_increase_allowance_account_not_initialized(
    jpyc_client_without_account,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.increase_allowance(
            spender=KNOWN_ACCOUNTS[1].address,
            increment=1000,
        )
