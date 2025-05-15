class JpycSdkError(Exception):
    """Base class for any SDK-related errors."""
    pass

#################
# Config Errors #
#################

class NetworkNotSupported(JpycSdkError):
    """Raised when the specified network is not supported by the SDK.

    Attributes:
        chain_name (str): Chain name
        network_name (str): Network name
    """
    def __init__(self, chain_name: str, network_name: str):
        from .chains import enumerate_supported_networks

        super().__init__(
            f"Network '{chain_name}/{network_name}' is not supported. "
            f"Supported networks are: {enumerate_supported_networks()}"
        )

class AccountNotInitialized(JpycSdkError):
    """Raised when account is not initialized or hoisted to web3 instance."""
    def __init__(self):
        super().__init__("Account is not initialized.")

######################
# Transaction Errors #
######################

class TransactionSimulationFailed(JpycSdkError):
    """Raised when transaction simulation fails.

    Attributes:
        message (str): Error message
    """
    def __init__(self, message: str):
        super().__init__(f"Failed to simulate a transaction locally: '{message}")

class TransactionFailedToSend(JpycSdkError):
    """Raised when it fails to send a transaction.

    Attributes:
        message (str): Error message
    """
    def __init__(self, message: str):
        super().__init__(f"Failed to send a transaction: '{message}")
