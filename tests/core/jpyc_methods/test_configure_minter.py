import pytest

from packages.core.src.utils.errors import (
    AccountNotInitialized,
    InvalidChecksumAddress,
    InvalidUint256,
)

from ..conftest import KNOWN_ACCOUNTS


@pytest.mark.parametrize(
    [
        "mocked_eth_contract_functions",
    ],
    [
        pytest.param(
            {
                "func_name": "configureMinter",
            },
        ),
    ],
    indirect=[
        "mocked_eth_contract_functions",
    ],
)
def test_configure_minter(
    jpyc_client,
    mocked_eth_contract_functions,
):
    minter = KNOWN_ACCOUNTS[0].address
    minter_allowed_amount = 10000

    jpyc_client.configure_minter(
        minter=minter,
        minter_allowed_amount=minter_allowed_amount,
    )

    mocked_eth_contract_functions.call_count == 2
    mocked_eth_contract_functions.assert_called_with(
        minter=minter,
        minterAllowedAmount=minter_allowed_amount * 10**18,
    )


@pytest.mark.parametrize(
    [
        "minter",
        "minter_allowed_amount",
        "exception_class",
    ],
    [
        pytest.param(
            "invalid_address",
            10000,
            InvalidChecksumAddress,
            id="invalid minter",
        ),
        pytest.param(
            KNOWN_ACCOUNTS[0].address,
            -1,
            InvalidUint256,
            id="invalid minter_allowed_amount",
        ),
    ],
)
def test_configure_minter_failures(
    jpyc_client,
    minter,
    minter_allowed_amount,
    exception_class,
):
    with pytest.raises(exception_class):
        jpyc_client.configure_minter(
            minter=minter, minter_allowed_amount=minter_allowed_amount
        )


def test_configure_minter_account_not_initialized(
    jpyc_client_without_account,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.configure_minter(
            minter=KNOWN_ACCOUNTS[0].address,
            minter_allowed_amount=10000,
        )
