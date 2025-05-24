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
            {"func_name": "transferFrom"},
        ),
    ],
    indirect=["mocked_eth_contract_functions"],
)
def test_transfer_from(
    jpyc_client,
    mocked_eth_contract_functions,
):
    from_ = KNOWN_ACCOUNTS[0].address
    to = KNOWN_ACCOUNTS[1].address
    value = 10000

    jpyc_client.transfer_from(
        from_=from_,
        to=to,
        value=value,
    )

    mocked_eth_contract_functions.call_count == 2


@pytest.mark.parametrize(
    [
        "from_",
        "to",
        "value",
        "exception_class",
    ],
    [
        pytest.param(
            "invalid_address",
            KNOWN_ACCOUNTS[1].address,
            10000,
            InvalidChecksumAddress,
            id="invalid from",
        ),
        pytest.param(
            KNOWN_ACCOUNTS[0].address,
            "invalid_address",
            10000,
            InvalidChecksumAddress,
            id="invalid to",
        ),
        pytest.param(
            KNOWN_ACCOUNTS[0].address,
            KNOWN_ACCOUNTS[1].address,
            -1,
            InvalidUint256,
            id="invalid value",
        ),
    ],
)
def test_transfer_from_failures(
    jpyc_client,
    from_,
    to,
    value,
    exception_class,
):
    with pytest.raises(exception_class):
        jpyc_client.transfer_from(
            from_=from_,
            to=to,
            value=value,
        )


def test_transfer_from_account_not_initialized(
    jpyc_client_without_account,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.transfer_from(
            from_=KNOWN_ACCOUNTS[0].address,
            to=KNOWN_ACCOUNTS[1].address,
            value=1000,
        )
