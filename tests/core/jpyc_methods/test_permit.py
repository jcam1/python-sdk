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
def signed_message_permit(
    eip712_domain_separator,
    eip712_domain_types,
    valid_before,
):
    return Account.sign_typed_data(
        KNOWN_ACCOUNTS[0].private_key,
        full_message={
            "domain": eip712_domain_separator,
            "types": {
                "EIP712Domain": eip712_domain_types,
                "Permit": [
                    {"name": "owner", "type": "address"},
                    {"name": "spender", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "deadline", "type": "uint256"},
                ],
            },
            "primaryType": "Permit",
            "message": {
                "owner": KNOWN_ACCOUNTS[0].address,
                "spender": KNOWN_ACCOUNTS[1].address,
                "value": 10000 * 10**18,
                "deadline": valid_before,
            },
        },
    )


@pytest.fixture(scope="function")
def signed_message_permit_v(signed_message_permit):
    return signed_message_permit.v


@pytest.fixture(scope="function")
def signed_message_permit_r(signed_message_permit):
    return add_zero_padding_to_hex(hex(signed_message_permit.r), 32)


@pytest.fixture(scope="function")
def signed_message_permit_s(signed_message_permit):
    return add_zero_padding_to_hex(hex(signed_message_permit.s), 32)


@pytest.mark.parametrize(
    ["mocked_eth_contract_functions"],
    [
        pytest.param(
            {"func_name": "permit"},
        ),
    ],
    indirect=["mocked_eth_contract_functions"],
)
def test_permit(
    jpyc_client,
    valid_before,
    signed_message_permit_v,
    signed_message_permit_r,
    signed_message_permit_s,
    mocked_eth_contract_functions,
):
    owner = KNOWN_ACCOUNTS[0].address
    spender = KNOWN_ACCOUNTS[1].address
    value = 10000

    jpyc_client.permit(
        owner=owner,
        spender=spender,
        value=value,
        deadline=valid_before,
        v=signed_message_permit_v,
        r=signed_message_permit_r,
        s=signed_message_permit_s,
    )

    mocked_eth_contract_functions.call_count == 2


def test_permit_invalid_owner(
    jpyc_client,
    valid_before,
    signed_message_permit_v,
    signed_message_permit_r,
    signed_message_permit_s,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.permit(
            owner="invalid_address",
            spender=KNOWN_ACCOUNTS[1].address,
            value=10000,
            deadline=valid_before,
            v=signed_message_permit_v,
            r=signed_message_permit_r,
            s=signed_message_permit_s,
        )


def test_permit_invalid_spender(
    jpyc_client,
    valid_before,
    signed_message_permit_v,
    signed_message_permit_r,
    signed_message_permit_s,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.permit(
            owner=KNOWN_ACCOUNTS[0].address,
            spender="invalid_address",
            value=10000,
            deadline=valid_before,
            v=signed_message_permit_v,
            r=signed_message_permit_r,
            s=signed_message_permit_s,
        )


def test_permit_invalid_value(
    jpyc_client,
    valid_before,
    signed_message_permit_v,
    signed_message_permit_r,
    signed_message_permit_s,
):
    with pytest.raises(InvalidUint256):
        jpyc_client.permit(
            owner=KNOWN_ACCOUNTS[0].address,
            spender=KNOWN_ACCOUNTS[1].address,
            value=-1,
            deadline=valid_before,
            v=signed_message_permit_v,
            r=signed_message_permit_r,
            s=signed_message_permit_s,
        )


def test_permit_invalid_deadline(
    jpyc_client,
    signed_message_permit_v,
    signed_message_permit_r,
    signed_message_permit_s,
):
    with pytest.raises(InvalidUint256):
        jpyc_client.permit(
            owner=KNOWN_ACCOUNTS[0].address,
            spender=KNOWN_ACCOUNTS[1].address,
            value=10000,
            deadline=-1,
            v=signed_message_permit_v,
            r=signed_message_permit_r,
            s=signed_message_permit_s,
        )


def test_permit_invalid_v(
    jpyc_client,
    valid_before,
    signed_message_permit_r,
    signed_message_permit_s,
):
    with pytest.raises(InvalidUint8):
        jpyc_client.permit(
            owner=KNOWN_ACCOUNTS[0].address,
            spender=KNOWN_ACCOUNTS[1].address,
            value=10000,
            deadline=valid_before,
            v=-1,
            r=signed_message_permit_r,
            s=signed_message_permit_s,
        )


def test_permit_invalid_r(
    jpyc_client,
    valid_before,
    signed_message_permit_v,
    signed_message_permit_s,
):
    with pytest.raises(InvalidBytes32):
        jpyc_client.permit(
            owner=KNOWN_ACCOUNTS[0].address,
            spender=KNOWN_ACCOUNTS[1].address,
            value=10000,
            deadline=valid_before,
            v=signed_message_permit_v,
            r="0x",
            s=signed_message_permit_s,
        )


def test_permit_invalid_s(
    jpyc_client,
    valid_before,
    signed_message_permit_v,
    signed_message_permit_r,
):
    with pytest.raises(InvalidBytes32):
        jpyc_client.permit(
            owner=KNOWN_ACCOUNTS[0].address,
            spender=KNOWN_ACCOUNTS[1].address,
            value=10000,
            deadline=valid_before,
            v=signed_message_permit_v,
            r=signed_message_permit_r,
            s="0x",
        )


def test_permit_account_not_initialized(
    jpyc_client_without_account,
    valid_before,
    signed_message_permit_v,
    signed_message_permit_r,
    signed_message_permit_s,
):
    with pytest.raises(AccountNotInitialized):
        jpyc_client_without_account.permit(
            owner=KNOWN_ACCOUNTS[0].address,
            spender=KNOWN_ACCOUNTS[1].address,
            value=10000,
            deadline=valid_before,
            v=signed_message_permit_v,
            r=signed_message_permit_r,
            s=signed_message_permit_s,
        )
