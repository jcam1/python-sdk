from typing import Annotated

from pydantic.functional_validators import AfterValidator
from web3 import Web3

from .constants import UINT8_MAX, UINT256_MAX, UINT_MIN
from .errors import (
    InvalidBytes32,
    InvalidChecksumAddress,
    InvalidRpcEndpoint,
    InvalidUint8,
    InvalidUint256,
)


def validate_checksum_address(address: str) -> str:
    """Checks if the given address is a checksum address.

    Args:
        address (str): Address string

    Returns:
        str: Address string

    Raises:
        InvalidChecksumAddress: If the address is not a valid checksum address
    """
    if not Web3.is_checksum_address(address):
        raise InvalidChecksumAddress(address)

    return address


ChecksumAddress = Annotated[str, AfterValidator(validate_checksum_address)]
"""A type that contains a checksum address. \
See `EIP55 <https://eips.ethereum.org/EIPS/eip-55>`_ for more details.
"""


def validate_uint8(integer: int) -> int:
    """Checks if the given integer is a uint8.

    Args:
        integer (int): Integer

    Returns:
        int: Integer

    Raises:
        InvalidUint8: If the integer is not a valid uint8
    """
    if integer < UINT_MIN or UINT8_MAX < integer:
        raise InvalidUint8(integer)

    return integer


Uint8 = Annotated[int, AfterValidator(validate_uint8)]
"""A type that contains a uint8."""


def validate_uint256(integer: int) -> int:
    """Checks if the given integer is a uint256.

    Args:
        integer (int): Integer

    Returns:
        int: Integer

    Raises:
        InvalidUint256: If the integer is not a valid uint256
    """
    if integer < UINT_MIN or UINT256_MAX < integer:
        raise InvalidUint256(integer)

    return integer


Uint256 = Annotated[int, AfterValidator(validate_uint256)]
"""A type that contains a uint256."""


def validate_bytes32(string: str) -> str:
    """Checks if the given string is bytes32.

    Args:
        string (str): String

    Returns:
        str: String

    Raises:
        InvalidBytes32: If the string is not a valid bytes32
    """
    try:
        assert string[:2] == "0x"
        assert len(bytes.fromhex(string[2:])) == 32
    except Exception:
        raise InvalidBytes32(string)

    return string


Bytes32 = Annotated[str, AfterValidator(validate_bytes32)]
"""A type that contains a bytes32."""


def validate_rpc_endpoint(string: str) -> str:
    """Checks if the given string is a valid RPC endpoint.

    Args:
        string (str): String

    Returns:
        str: String

    Raises:
        InvalidRpcEndpoint: If the string is not a valid RPC endpoint
    """
    try:
        assert string.startswith("http") is True
    except Exception:
        raise InvalidRpcEndpoint(string)

    return string


RpcEndpoint = Annotated[str, AfterValidator(validate_rpc_endpoint)]
"""A type that contains a rpc endpoint."""
