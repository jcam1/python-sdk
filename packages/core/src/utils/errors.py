class JpycSdkError(Exception):
    """A base class for any errors related to JPYC SDK."""

    def __init__(self, code: int, message: str):
        self.code = code
        """int: Custom error code"""
        self.message = message
        """str: Error message"""
        super().__init__(f"\nError Code: {code}\nMessage: {message}")


#################
# Config Errors #
#################


class NetworkNotSupported(JpycSdkError):
    """Raised when the specified network is not supported by the SDK.

    Attributes:
        chain_name (str): Chain name
        network_name (str): Network name
    """

    code = 100

    def __init__(self, chain_name: str, network_name: str):
        from .chains import enumerate_supported_networks

        super().__init__(
            code=NetworkNotSupported.code,
            message=f"Network '{chain_name}/{network_name}' is not supported. "
            f"Supported networks are: {enumerate_supported_networks()}",
        )


class AccountNotInitialized(JpycSdkError):
    """Raised when account is not initialized or hoisted to web3 instance."""

    code = 101

    def __init__(self):
        super().__init__(
            code=AccountNotInitialized.code,
            message="Account is not initialized.",
        )


#####################
# Validation Errors #
#####################
class InvalidChecksumAddress(JpycSdkError, TypeError):
    """Raised when the given address is not a valid checksum address."""

    code = 200

    def __init__(self, message_: str):
        super().__init__(
            code=InvalidChecksumAddress.code,
            message=f"Invalid checksum address: {message_}. "
            f"Address must be compatible with EIP55.",
        )


class InvalidUint8(JpycSdkError, TypeError):
    """Raised when the given integer is not a valid uint8."""

    code = 201

    def __init__(self, message_: str):
        super().__init__(
            code=InvalidUint8.code,
            message=f"Invalid uint8: {message_}. Integer must be between 0 ~ 2^8 - 1.",
        )


class InvalidUint256(JpycSdkError, TypeError):
    """Raised when the given integer is not a valid uint256."""

    code = 202

    def __init__(self, message_: str):
        super().__init__(
            code=InvalidUint256.code,
            message=f"Invalid uint256: {message_}. "
            f"Integer must be between 0 ~ 2^256 - 1.",
        )


class InvalidBytes32(JpycSdkError, TypeError):
    """Raised when the given byte string is not a valid bytes32."""

    code = 203

    def __init__(self, message_: str):
        super().__init__(
            code=InvalidBytes32.code,
            message=f"Invalid bytes32: {message_}.",
        )


class InvalidRpcEndpoint(JpycSdkError, TypeError):
    """Raised when the given string is not a valid RPC endpoint."""

    code = 204

    def __init__(self, message_: str):
        super().__init__(
            code=InvalidRpcEndpoint.code,
            message=f"Invalid RPC endpoint: {message_}.",
        )


######################
# Transaction Errors #
######################


class TransactionSimulationFailed(JpycSdkError):
    """Raised when transaction simulation fails.

    Attributes:
        message (str): Error message
    """

    code = 300

    def __init__(self, message_: str):
        super().__init__(
            code=TransactionSimulationFailed.code,
            message=f"Failed to simulate a transaction locally: {message_}",
        )


class TransactionFailed(JpycSdkError):
    """Raised when transaction fails.

    Attributes:
        message (str): Error message
    """

    code = 301

    def __init__(self, message_: str):
        super().__init__(
            code=TransactionFailed.code,
            message=f"Transaction failed: {message_}",
        )
