"""Type definition module

This module provides type definitions used in the JPYC SDK.
It defines basic types such as Ethereum addresses, numeric types, and names of chains and environments.
These type definitions are used throughout the SDK to ensure type safety and improve developer experience.
"""

from typing import Literal, TypeAlias, NewType, Union, Any
from typing_extensions import Annotated
from web3.types import ChecksumAddress

# Definition of address and related types
Address = NewType('Address', ChecksumAddress)
Bytes32 = NewType('Bytes32', str)
Endpoint: TypeAlias = str

# Definition of supported chains and networks
ChainName = Literal['local', 'ethereum', 'polygon', 'gnosis', 'avalanche', 'astar', 'shiden']
NetworkName = Literal['mainnet', 'goerli', 'sepolia', 'amoy', 'chiado', 'fuji']

class Uint8:
    """
    A lightweight class representing Solidity's uint8 type.
    
    - Only holds a value in the range [0, 255].
    - Stores the internal value as an integer.
    - Provides range checks and simple int conversion.
    
    Examples:
        >>> u = Uint8(123)
        >>> u.to_int()
        123
        >>> u == 123
        True
    """

    __slots__ = ("_value",)
    
    def __init__(self, value: int):
        """
        Initialize a Uint8 instance from a Python int.
        
        Args:
            value: Integer value between 0 and 255
            
        Raises:
            TypeError: If value is not an integer
            ValueError: If value is outside the range of uint8
        """
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value).__name__}")
        if value < 0 or value > 255:
            raise ValueError(f"Value {value} is outside the range of uint8 (0..255)")
        self._value = value
    
    def to_int(self) -> int:
        """Returns the stored integer value."""
        return self._value
    
    def __eq__(self, other: object) -> bool:
        """
        Equality comparison with either another Uint8 or an int.
        """
        if isinstance(other, Uint8):
            return self._value == other._value
        elif isinstance(other, int):
            return self._value == other
        return NotImplemented
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Uint8({self._value})"
    
class Uint256:
    """
    A lightweight class representing Solidity's uint256 type without operator overloading.
    
    - Only holds a value in the range [0, 2^256 - 1].
    - Stores the internal value as an integer (Python int is arbitrary-precision).
    - Provides range checks and simple string/int conversion.
    
    Examples:
        >>> u = Uint256.from_value(123)
        >>> u.to_string()
        '123'
        >>> u.to_int()
        123
    """

    def __init__(self, value: int):
        """
        Initialize a Uint256 instance from a Python int.
        
        Args:
            value: Integer value between 0 and 2^256 - 1
            
        Raises:
            TypeError: If value is not an integer
            ValueError: If value is outside the range of uint256
        """
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value).__name__}")
        if value < 0 or value >= 2**256:
            raise ValueError(f"Value {value} is outside the range of uint256 (0 to 2^256-1)")
        
        self._value = value

    def to_int(self) -> int:
        """Returns the stored integer value."""
        return self._value

    def to_string(self) -> str:
        """Returns the decimal string representation of this uint256."""
        return str(self._value)

    def __str__(self) -> str:
        """Same as `to_string()`."""
        return str(self._value)

    def __repr__(self) -> str:
        """Debug representation."""
        return f"Uint256({self._value})"

    def __eq__(self, other: Any) -> bool:
        """
        Equality comparison with either another Uint256 or an int.
        """
        if isinstance(other, Uint256):
            return self._value == other._value
        elif isinstance(other, int):
            return self._value == other
        return NotImplemented

    @classmethod
    def from_string(cls, s: str) -> 'Uint256':
        """
        Create a Uint256 from a decimal string.
        
        Raises:
            ValueError: if the string is not a valid integer or out of range
        """
        try:
            as_int = int(s, 10)  # decimal parse
        except ValueError:
            raise ValueError(f"Cannot convert '{s}' to Uint256")
        return cls(as_int)

    @classmethod
    def from_value(cls, val: Union[int, str]) -> 'Uint256':
        """
        Factory method. Accepts either an int or decimal string, similar to TS's Uint256.from().
        
        Examples:
            Uint256.from_value(123)
            Uint256.from_value("123")
        """
        if isinstance(val, int):
            return cls(val)
        elif isinstance(val, str):
            return cls.from_string(val)
        else:
            raise TypeError(f"Expected int or str, got {type(val).__name__}")