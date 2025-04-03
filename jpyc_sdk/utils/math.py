"""Mathematical utility module

This module provides utility functions related to token numerical calculations.
It includes functionality for handling 18 decimal places commonly used in Ethereum-based tokens,
conversions to uint256 type, and other numerical representations used in blockchain.
"""

from decimal import Decimal
from typing import Union

from .types import Uint256

# Number of decimal places for the token
TOKEN_DECIMALS = 18
DECIMALS_QUANTIFIER = 10 ** TOKEN_DECIMALS

def to_uint256(value: Union[int, str]) -> Uint256:
    """
    Convert an integer value or its string representation to a uint256 representation.
    
    Args:
        value: Integer value or string representation
        
    Returns:
        Uint256: Value represented as uint256
        
    Raises:
        TypeError: If value is not an integer or string
        ValueError: If value is outside the range of uint256
    """
    if isinstance(value, str):
        return Uint256.from_string(value)
    elif isinstance(value, int):
        return Uint256(value)
    else:
        raise TypeError(f"Expected int or str, got {type(value).__name__}")

def remove_decimals(value: Union[int, float, Decimal]) -> Uint256:
    """
    Removes the decimal point so that only integer values exist on-chain.
    Example:
        0.01 -> 10,000,000,000,000,000
        100  -> 100,000,000,000,000,000,000
        
    Args:
        value: Integer or decimal value
        
    Returns:
        Uint256: Value represented as uint256
        
    Raises:
        ValueError: If the calculated result is outside the range of uint256
    """
    if isinstance(value, Decimal):
        decimal_value = int(value * Decimal(DECIMALS_QUANTIFIER))
        return Uint256(decimal_value)
    else:
        float_value = int(value * DECIMALS_QUANTIFIER)
        return Uint256(float_value)

def restore_decimals(value: Union[Uint256, int]) -> float:
    """
    Restores decimal places, mainly for display purposes.
    Example:
        10,000,000,000,000,000 -> 0.01
        100,000,000,000,000,000,000 -> 100
        
    Args:
        value: uint256 value or integer value
        
    Returns:
        float: Value represented as a number (integer or decimal)
    """
    if isinstance(value, Uint256):
        return float(value.to_int()) / float(DECIMALS_QUANTIFIER)
    else:
        return float(value) / float(DECIMALS_QUANTIFIER)