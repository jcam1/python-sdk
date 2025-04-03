"""Address definitions and utility module

This module provides constant definitions for important contract addresses used in the JPYC SDK,
as well as utility functions for address validation.
It includes basic address constants such as proxy contract addresses and the zero address.
"""

import os
from web3 import Web3

from .types import Address

# Address definitions
ZERO_ADDRESS = Address(Web3.to_checksum_address('0x0000000000000000000000000000000000000000'))
V2_PROXY_ADDRESS = Address(Web3.to_checksum_address('0x431D5dfF03120AFA4bDf332c61A6e1766eF37BDB'))
LOCAL_PROXY_ADDRESS = Address(Web3.to_checksum_address(os.environ.get('LOCAL_PROXY_ADDRESS', '0x0000000000000000000000000000000000000000')))

def is_valid_address(address: str) -> bool:
    """
    Checks if the specified address is a valid Ethereum address.
    
    Args:
        address: Address string to check
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        Web3.to_checksum_address(address)
        return True
    except ValueError:
        return False