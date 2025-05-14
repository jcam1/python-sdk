from .chains import enumerate_supported_networks

class JpycSdkError(Exception):
    """Base class for any SDK-related errors."""
    pass

class NetworkNotSupported(JpycSdkError):
    """Raised when the specified network is not supported by the SDK.

    Attributes:
        chain_name (str): Chain name
        network_name (str): Network name
    """
    def __init__(self, chain_name: str, network_name: str):
        super().__init__(
            f"Network '{chain_name}/{network_name}' is not supported. "
            f"Supported networks are: {enumerate_supported_networks()}"
        )

class TransactionFailed(JpycSdkError):
    """Raised when failed to send a transaction.

    Attributes:
        message (str): Error message
    """
    def __init__(self, message: str):
        super().__init__(f"Failed to send a transaction: '{message}")
