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
            {"func_name": "mint"},
        ),
    ],
    indirect=["mocked_eth_contract_functions"],
)
def test_mint(
    jpyc_client,
    mocked_eth_contract_functions,
):
    to = KNOWN_ACCOUNTS[0].address
    amount = 10000

    jpyc_client.mint(
        to=to,
        amount=amount,
    )

    mocked_eth_contract_functions.call_count == 2
    mocked_eth_contract_functions.assert_called_with(
        _to=to,
        _amount=amount * 10**18,
    )


@pytest.mark.parametrize(
    [
        "to",
        "amount",
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
            KNOWN_ACCOUNTS[0].address,
            -1,
            InvalidUint256,
            id="invalid amount",
        ),
    ],
)
def test_mint_failures(
    jpyc_client,
    to,
    amount,
    exception_class,
):
    with pytest.raises(exception_class):
        jpyc_client.mint(
            to=to,
            amount=amount,
        )


def test_mint_account_not_initialized(
    jpyc_client_without_account,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.mint(
            to=KNOWN_ACCOUNTS[1].address,
            amount=1000,
        )
