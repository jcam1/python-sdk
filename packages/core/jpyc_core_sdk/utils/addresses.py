from typing import Final

from eth_typing import (
    ChecksumAddress,
    HexAddress,
    HexStr,
)
from web3 import Web3
from web3.constants import ADDRESS_ZERO

from .types import ContractType

####################################
# Address-related helper functions #
####################################


def calc_checksum_address(address: str) -> ChecksumAddress:
    """Calculates checksum address.

    Args:
        address (str): Address string

    Returns:
        ChecksumAddress: Checksum address
    """
    return ChecksumAddress(HexAddress(HexStr(Web3.to_checksum_address(address))))


def is_valid_address(address: str) -> bool:
    """Checks validity of address.

    Args:
        address (str): Address string

    Returns:
        bool: True if valid, false otherwise
    """
    return Web3.is_checksum_address(address)


def get_proxy_address(contract_type: ContractType) -> ChecksumAddress:
    """Get proxy address from the specified contract type.

    Args:
        contract_type (ContractType): Contract type (`jpyc` or `jpyc_prepaid`)

    Returns:
        ChecksumAddress: Checksum address of proxy contract
    """
    match contract_type:
        case "jpyc":
            return JPYC_PROXY_ADDRESS
        case "jpyc_prepaid":
            return JPYC_PREPAID_PROXY_ADDRESS


######################
# Constant addresses #
######################

ZERO_ADDRESS: Final[ChecksumAddress] = calc_checksum_address(str(ADDRESS_ZERO))
"""ChecksumAddress: Zero address."""
JPYC_PROXY_ADDRESS: Final[ChecksumAddress] = calc_checksum_address(
    "0xE7C3D8C9a439feDe00D2600032D5dB0Be71C3c29"
)
"""ChecksumAddress: Proxy address of JPYC contract."""
JPYC_PREPAID_PROXY_ADDRESS: Final[ChecksumAddress] = calc_checksum_address(
    "0x431D5dfF03120AFA4bDf332c61A6e1766eF37BDB"
)
"""ChecksumAddress: Proxy address of JPYC Prepaid contract."""
