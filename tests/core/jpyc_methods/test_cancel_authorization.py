from eth_account import Account
import pytest

from packages.core.jpyc_core_sdk.utils.errors import (
    AccountNotInitialized,
    InvalidBytes32,
    InvalidChecksumAddress,
    InvalidUint8,
)

from ..conftest import add_zero_padding_to_hex, KNOWN_ACCOUNTS


@pytest.fixture(scope="function")
def signed_message_cancel(
    eip712_domain_separator,
    eip712_domain_types,
    nonce,
):
    return Account.sign_typed_data(
        KNOWN_ACCOUNTS[0].private_key,
        full_message={
            "domain": eip712_domain_separator,
            "types": {
                "EIP712Domain": eip712_domain_types,
                "CancelAuthorization": [
                    {"name": "authorizer", "type": "address"},
                    {"name": "nonce", "type": "bytes32"},
                ],
            },
            "primaryType": "CancelAuthorization",
            "message": {
                "authorizer": KNOWN_ACCOUNTS[0].address,
                "nonce": nonce,
            },
        },
    )


@pytest.fixture(scope="function")
def signed_message_cancel_v(signed_message_cancel):
    return signed_message_cancel.v


@pytest.fixture(scope="function")
def signed_message_cancel_r(signed_message_cancel):
    return add_zero_padding_to_hex(hex(signed_message_cancel.r), 32)


@pytest.fixture(scope="function")
def signed_message_cancel_s(signed_message_cancel):
    return add_zero_padding_to_hex(hex(signed_message_cancel.s), 32)


@pytest.mark.parametrize(
    ["mocked_eth_contract_functions"],
    [
        pytest.param(
            {"func_name": "cancelAuthorization"},
        ),
    ],
    indirect=["mocked_eth_contract_functions"],
)
def test_cancel_authorization(
    jpyc_client,
    nonce,
    signed_message_cancel_v,
    signed_message_cancel_r,
    signed_message_cancel_s,
    mocked_eth_contract_functions,
):
    authorizer = KNOWN_ACCOUNTS[0].address

    jpyc_client.cancel_authorization(
        authorizer=authorizer,
        nonce=nonce,
        v=signed_message_cancel_v,
        r=signed_message_cancel_r,
        s=signed_message_cancel_s,
    )

    mocked_eth_contract_functions.call_count == 2


def test_cancel_authorization_invalid_authorizer(
    jpyc_client,
    nonce,
    signed_message_cancel_v,
    signed_message_cancel_r,
    signed_message_cancel_s,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.cancel_authorization(
            authorizer="invalid_address",
            nonce=nonce,
            v=signed_message_cancel_v,
            r=signed_message_cancel_r,
            s=signed_message_cancel_s,
        )


def test_cancel_authorization_invalid_nonce(
    jpyc_client,
    signed_message_cancel_v,
    signed_message_cancel_r,
    signed_message_cancel_s,
):
    with pytest.raises(InvalidBytes32):
        jpyc_client.cancel_authorization(
            authorizer=KNOWN_ACCOUNTS[0].address,
            nonce="0x",
            v=signed_message_cancel_v,
            r=signed_message_cancel_r,
            s=signed_message_cancel_s,
        )


def test_cancel_authorization_invalid_v(
    jpyc_client,
    nonce,
    signed_message_cancel_r,
    signed_message_cancel_s,
):
    with pytest.raises(InvalidUint8):
        jpyc_client.cancel_authorization(
            authorizer=KNOWN_ACCOUNTS[0].address,
            nonce=nonce,
            v=-1,
            r=signed_message_cancel_r,
            s=signed_message_cancel_s,
        )


def test_cancel_authorization_invalid_r(
    jpyc_client,
    nonce,
    signed_message_cancel_v,
    signed_message_cancel_s,
):
    with pytest.raises(InvalidBytes32):
        jpyc_client.cancel_authorization(
            authorizer=KNOWN_ACCOUNTS[0].address,
            nonce=nonce,
            v=signed_message_cancel_v,
            r="0x",
            s=signed_message_cancel_s,
        )


def test_cancel_authorization_invalid_s(
    jpyc_client,
    nonce,
    signed_message_cancel_v,
    signed_message_cancel_r,
):
    with pytest.raises(InvalidBytes32):
        jpyc_client.cancel_authorization(
            authorizer=KNOWN_ACCOUNTS[0].address,
            nonce=nonce,
            v=signed_message_cancel_v,
            r=signed_message_cancel_r,
            s="0x",
        )


def test_cancel_authorization_account_not_initialized(
    jpyc_client_without_account,
    nonce,
    signed_message_cancel_v,
    signed_message_cancel_r,
    signed_message_cancel_s,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.cancel_authorization(
            authorizer=KNOWN_ACCOUNTS[0].address,
            nonce=nonce,
            v=signed_message_cancel_v,
            r=signed_message_cancel_r,
            s=signed_message_cancel_s,
        )
