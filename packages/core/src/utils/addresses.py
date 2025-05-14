from typing import Final

from eth_typing import (
    ChecksumAddress,
    HexAddress,
    HexStr,
)
from web3 import Web3
from web3.constants import ADDRESS_ZERO

from .types import ContractVersion

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
    return ChecksumAddress(HexAddress(HexStr(address)))

def is_valid_address(address: str) -> bool:
    """Checks validity of address.

    Args:
        address (str): Address string

    Returns:
        bool: True if valid, false otherwise
    """
    return Web3.is_checksum_address(address)

def get_proxy_address(contract_version: ContractVersion) -> ChecksumAddress:
    """Get proxy address from the specified version.

    Note:
        Default address should be the address of the latest version (e.g., v2 as of May 2025).

    Args:
        version (ContractVersion): Contract version

    Returns:
        ChecksumAddress: Checksum address of proxy contract
    """
    match contract_version:
        case "2":
            return V2_PROXY_ADDRESS
        case _:
            return V2_PROXY_ADDRESS

######################
# Constant addresses #
######################

ZERO_ADDRESS: Final[ChecksumAddress] = calc_checksum_address(str(ADDRESS_ZERO))
"""ChecksumAddress: Zero address."""
V2_PROXY_ADDRESS: Final[ChecksumAddress] = calc_checksum_address("0x431D5dfF03120AFA4bDf332c61A6e1766eF37BDB")
"""ChecksumAddress: JPYCv2 address."""
