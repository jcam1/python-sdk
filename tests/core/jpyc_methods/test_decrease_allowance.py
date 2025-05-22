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
            {"func_name": "decreaseAllowance"},
        ),
    ],
    indirect=["mocked_eth_contract_functions"],
)
def test_decrease_allowance(
    jpyc_client,
    mocked_eth_contract_functions,
):
    spender = KNOWN_ACCOUNTS[1].address
    decrement = 1000

    jpyc_client.decrease_allowance(
        spender=spender,
        decrement=decrement,
    )

    mocked_eth_contract_functions.call_count == 2
    mocked_eth_contract_functions.assert_called_with(
        spender=spender,
        decrement=decrement * 10**18,
    )


@pytest.mark.parametrize(
    [
        "spender",
        "decrement",
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
            id="invalid decrement",
        ),
    ],
)
def test_decrease_allowance_failures(
    jpyc_client,
    spender,
    decrement,
    exception_class,
):
    with pytest.raises(exception_class):
        jpyc_client.decrease_allowance(
            spender=spender,
            decrement=decrement,
        )


def test_decrease_allowance_account_not_initialized(
    jpyc_client_without_account,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.decrease_allowance(
            spender=KNOWN_ACCOUNTS[1].address,
            decrement=1000,
        )
