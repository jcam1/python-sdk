from decimal import Decimal

from web3 import Web3

from .validators import Uint256


def remove_decimals(value: Uint256 | Decimal) -> Uint256:
    """Remove decimals.

    Args:
        value (Uint256 | Decimal): Value in ether

    Returns:
        Uint256: Value in wei
    """
    return Web3.to_wei(value, "ether")


def restore_decimals(func):  # type: ignore[no-untyped-def]
    """Decorator to restore decimals."""

    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        result = func(*args, **kwargs)
        return Web3.from_wei(result, "ether")

    return wrapper
