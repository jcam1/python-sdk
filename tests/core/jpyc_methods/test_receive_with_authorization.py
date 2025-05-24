from eth_account import Account
import pytest

from packages.core.jpyc_core_sdk.utils.errors import (
    AccountNotInitialized,
    InvalidBytes32,
    InvalidChecksumAddress,
    InvalidUint256,
    InvalidUint8,
)

from ..conftest import add_zero_padding_to_hex, KNOWN_ACCOUNTS


@pytest.fixture(scope="function")
def signed_message_receive(
    eip712_domain_separator,
    eip712_domain_types,
    valid_before,
    nonce,
):
    return Account.sign_typed_data(
        KNOWN_ACCOUNTS[0].private_key,
        full_message={
            "domain": eip712_domain_separator,
            "types": {
                "EIP712Domain": eip712_domain_types,
                "ReceiveWithAuthorization": [
                    {"name": "from", "type": "address"},
                    {"name": "to", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "validAfter", "type": "uint256"},
                    {"name": "validBefore", "type": "uint256"},
                    {"name": "nonce", "type": "bytes32"},
                ],
            },
            "primaryType": "ReceiveWithAuthorization",
            "message": {
                "from": KNOWN_ACCOUNTS[0].address,
                "to": KNOWN_ACCOUNTS[1].address,
                "value": 10000 * 10**18,
                "validAfter": 0,
                "validBefore": valid_before,
                "nonce": nonce,
            },
        },
    )


@pytest.fixture(scope="function")
def signed_message_receive_v(signed_message_receive):
    return signed_message_receive.v


@pytest.fixture(scope="function")
def signed_message_receive_r(signed_message_receive):
    return add_zero_padding_to_hex(hex(signed_message_receive.r), 32)


@pytest.fixture(scope="function")
def signed_message_receive_s(signed_message_receive):
    return add_zero_padding_to_hex(hex(signed_message_receive.s), 32)


@pytest.mark.parametrize(
    ["mocked_eth_contract_functions"],
    [
        pytest.param(
            {"func_name": "receiveWithAuthorization"},
        ),
    ],
    indirect=["mocked_eth_contract_functions"],
)
def test_receive_with_authorization(
    jpyc_client,
    valid_before,
    nonce,
    signed_message_receive_v,
    signed_message_receive_r,
    signed_message_receive_s,
    mocked_eth_contract_functions,
):
    from_ = KNOWN_ACCOUNTS[0].address
    to = KNOWN_ACCOUNTS[1].address
    value = 10000
    valid_after = 0

    jpyc_client.receive_with_authorization(
        from_=from_,
        to=to,
        value=value,
        valid_after=valid_after,
        valid_before=valid_before,
        nonce=nonce,
        v=signed_message_receive_v,
        r=signed_message_receive_r,
        s=signed_message_receive_s,
    )

    mocked_eth_contract_functions.call_count == 2


def test_receive_with_authorization_invalid_from(
    jpyc_client,
    valid_before,
    nonce,
    signed_message_receive_v,
    signed_message_receive_r,
    signed_message_receive_s,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.receive_with_authorization(
            from_="invalid_address",
            to=KNOWN_ACCOUNTS[1].address,
            value=10000,
            valid_after=0,
            valid_before=valid_before,
            nonce=nonce,
            v=signed_message_receive_v,
            r=signed_message_receive_r,
            s=signed_message_receive_s,
        )


def test_receive_with_authorization_invalid_to(
    jpyc_client,
    valid_before,
    nonce,
    signed_message_receive_v,
    signed_message_receive_r,
    signed_message_receive_s,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.receive_with_authorization(
            from_=KNOWN_ACCOUNTS[0].address,
            to="invalid_address",
            value=10000,
            valid_after=0,
            valid_before=valid_before,
            nonce=nonce,
            v=signed_message_receive_v,
            r=signed_message_receive_r,
            s=signed_message_receive_s,
        )


def test_receive_with_authorization_invalid_value(
    jpyc_client,
    valid_before,
    nonce,
    signed_message_receive_v,
    signed_message_receive_r,
    signed_message_receive_s,
):
    with pytest.raises(InvalidUint256):
        jpyc_client.receive_with_authorization(
            from_=KNOWN_ACCOUNTS[0].address,
            to=KNOWN_ACCOUNTS[1].address,
            value=-1,
            valid_after=0,
            valid_before=valid_before,
            nonce=nonce,
            v=signed_message_receive_v,
            r=signed_message_receive_r,
            s=signed_message_receive_s,
        )


def test_receive_with_authorization_invalid_valid_after(
    jpyc_client,
    valid_before,
    nonce,
    signed_message_receive_v,
    signed_message_receive_r,
    signed_message_receive_s,
):
    with pytest.raises(InvalidUint256):
        jpyc_client.receive_with_authorization(
            from_=KNOWN_ACCOUNTS[0].address,
            to=KNOWN_ACCOUNTS[1].address,
            value=10000,
            valid_after=-1,
            valid_before=valid_before,
            nonce=nonce,
            v=signed_message_receive_v,
            r=signed_message_receive_r,
            s=signed_message_receive_s,
        )


def test_receive_with_authorization_invalid_valid_before(
    jpyc_client,
    nonce,
    signed_message_receive_v,
    signed_message_receive_r,
    signed_message_receive_s,
):
    with pytest.raises(InvalidUint256):
        jpyc_client.receive_with_authorization(
            from_=KNOWN_ACCOUNTS[0].address,
            to=KNOWN_ACCOUNTS[1].address,
            value=10000,
            valid_after=0,
            valid_before=-1,
            nonce=nonce,
            v=signed_message_receive_v,
            r=signed_message_receive_r,
            s=signed_message_receive_s,
        )


def test_receive_with_authorization_invalid_nonce(
    jpyc_client,
    valid_before,
    signed_message_receive_v,
    signed_message_receive_r,
    signed_message_receive_s,
):
    with pytest.raises(InvalidBytes32):
        jpyc_client.receive_with_authorization(
            from_=KNOWN_ACCOUNTS[0].address,
            to=KNOWN_ACCOUNTS[1].address,
            value=10000,
            valid_after=0,
            valid_before=valid_before,
            nonce="0x",
            v=signed_message_receive_v,
            r=signed_message_receive_r,
            s=signed_message_receive_s,
        )


def test_receive_with_authorization_invalid_v(
    jpyc_client,
    valid_before,
    nonce,
    signed_message_receive_r,
    signed_message_receive_s,
):
    with pytest.raises(InvalidUint8):
        jpyc_client.receive_with_authorization(
            from_=KNOWN_ACCOUNTS[0].address,
            to=KNOWN_ACCOUNTS[1].address,
            value=10000,
            valid_after=0,
            valid_before=valid_before,
            nonce=nonce,
            v=-1,
            r=signed_message_receive_r,
            s=signed_message_receive_s,
        )


def test_receive_with_authorization_invalid_r(
    jpyc_client,
    valid_before,
    nonce,
    signed_message_receive_v,
    signed_message_receive_s,
):
    with pytest.raises(InvalidBytes32):
        jpyc_client.receive_with_authorization(
            from_=KNOWN_ACCOUNTS[0].address,
            to=KNOWN_ACCOUNTS[1].address,
            value=10000,
            valid_after=0,
            valid_before=valid_before,
            nonce=nonce,
            v=signed_message_receive_v,
            r="0x",
            s=signed_message_receive_s,
        )


def test_receive_with_authorization_invalid_s(
    jpyc_client,
    valid_before,
    nonce,
    signed_message_receive_v,
    signed_message_receive_r,
):
    with pytest.raises(InvalidBytes32):
        jpyc_client.receive_with_authorization(
            from_=KNOWN_ACCOUNTS[0].address,
            to=KNOWN_ACCOUNTS[1].address,
            value=10000,
            valid_after=0,
            valid_before=valid_before,
            nonce=nonce,
            v=signed_message_receive_v,
            r=signed_message_receive_r,
            s="0x",
        )


def test_receive_with_authorization_account_not_initialized(
    jpyc_client_without_account,
    valid_before,
    nonce,
    signed_message_receive_v,
    signed_message_receive_r,
    signed_message_receive_s,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.receive_with_authorization(
            from_=KNOWN_ACCOUNTS[0].address,
            to=KNOWN_ACCOUNTS[1].address,
            value=10000,
            valid_after=0,
            valid_before=valid_before,
            nonce=nonce,
            v=signed_message_receive_v,
            r=signed_message_receive_r,
            s=signed_message_receive_s,
        )
