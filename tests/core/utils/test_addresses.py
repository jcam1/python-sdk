import pytest

from packages.core.jpyc_core_sdk.utils.addresses import (
    calc_checksum_address,
    get_proxy_address,
    is_valid_address,
)


JPYC_PROXY_CHECKSUM_ADDRESS = "0xE7C3D8C9a439feDe00D2600032D5dB0Be71C3c29"
JPYC_PREPAID_PROXY_CHECKSUM_ADDRESS = "0x431D5dfF03120AFA4bDf332c61A6e1766eF37BDB"
INVALID_CHECKSUM_ADDRESS = "0x431d5dff03120afa4bdf332c61a6e1766ef37bdb"
JPYC_PREPAID_PROXY_ADDRESS_IN_INTEGER = 383157291474631222722397742278122605068030278619
INVALID_ADDRESS_IN_INTEGER = 0


@pytest.mark.parametrize(
    [
        "address",
    ],
    [
        pytest.param(
            JPYC_PREPAID_PROXY_CHECKSUM_ADDRESS,
            id="valid checksum address",
        ),
        pytest.param(
            INVALID_CHECKSUM_ADDRESS,
            id="invalid checksum address",
        ),
        pytest.param(
            JPYC_PREPAID_PROXY_ADDRESS_IN_INTEGER,
            id="valid address in integer",
        ),
    ],
)
def test_calc_checksum_address(address):
    checksum_address = calc_checksum_address(address=address)

    assert type(checksum_address) is str
    assert checksum_address == JPYC_PREPAID_PROXY_CHECKSUM_ADDRESS


def test_calc_checksum_address_failures():
    with pytest.raises(ValueError):
        calc_checksum_address(address=INVALID_ADDRESS_IN_INTEGER)


@pytest.mark.parametrize(
    [
        "address",
        "response",
    ],
    [
        pytest.param(JPYC_PREPAID_PROXY_CHECKSUM_ADDRESS, True, id="valid address"),
        pytest.param(INVALID_CHECKSUM_ADDRESS, False, id="invalid address"),
        pytest.param(
            JPYC_PREPAID_PROXY_ADDRESS_IN_INTEGER, False, id="valid address in integer"
        ),
        pytest.param(
            INVALID_ADDRESS_IN_INTEGER, False, id="invalid address in integer"
        ),
    ],
)
def test_is_valid_address(address, response):
    assert is_valid_address(address=address) is response


@pytest.mark.parametrize(
    [
        "contract_type",
        "response",
    ],
    [
        pytest.param("jpyc", JPYC_PROXY_CHECKSUM_ADDRESS, id="contract type = 'jpyc'"),
        pytest.param(
            "jpyc_prepaid",
            JPYC_PREPAID_PROXY_CHECKSUM_ADDRESS,
            id="contract type = 'jpyc_prepaid'",
        ),
        pytest.param("v2", None, id="invalid contract type"),
    ],
)
def test_get_proxy_address(contract_type, response):
    assert get_proxy_address(contract_type=contract_type) == response
