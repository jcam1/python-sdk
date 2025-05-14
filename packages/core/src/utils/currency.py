from decimal import Decimal

from web3 import Web3

def remove_decimals(value: Decimal) -> int:
    """Remove decimals.

    Args:
        value (Decimal): Decimal value

    Returns:
        int: Value in wei
    """
    return Web3.to_wei(value, 'ether')

def restore_decimals(func):
    """Decorator to restore decimals."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return Web3.from_wei(result, 'ether')

    return wrapper
