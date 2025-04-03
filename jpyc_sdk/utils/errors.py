"""Error definition module

This module defines exception classes used by the JPYC SDK.
All exceptions inherit from the base class `JpycSdkError` to clearly identify SDK-specific errors.
Each exception class corresponds to a specific error situation and provides appropriate error messages.
"""

from .chains import get_supported_chain_names, get_supported_network_names

class JpycSdkError(Exception):
    """Base class for all JPYC SDK errors"""
    pass

class InvalidChainNameError(JpycSdkError):
    """Raised when an unsupported blockchain name is specified"""
    def __init__(self, chain_name: str):
        supported_chains = ', '.join(get_supported_chain_names())
        super().__init__(
            f"Invalid chain '{chain_name}' (supported chain names = {{{supported_chains}}})."
        )

class InvalidNetworkNameError(JpycSdkError):
    """Raised when an unsupported network name is specified for a given chain"""
    def __init__(self, chain_name: str, network_name: str):
        supported_networks = ', '.join(get_supported_network_names(chain_name))
        super().__init__(
            f"Invalid network '{network_name}' (supported network names = {{{supported_networks}}})."
        )

class InvalidAddressError(JpycSdkError):
    """Raised when an invalid Ethereum address is provided"""
    def __init__(self, address: str):
        super().__init__(f"Invalid address '{address}'.")

class InvalidTransactionError(JpycSdkError):
    """Raised when a transaction simulation fails"""
    def __init__(self, error: Exception):
        super().__init__(f"Transaction simulation failed.\n{str(error)}")