import pytest
from decimal import Decimal
from jpyc_sdk.utils.math import to_uint256, remove_decimals, restore_decimals
from jpyc_sdk.utils.types import Uint256

class TestMathFunctions:
    def test_to_uint256(self):
        # Convert integer to Uint256
        value = to_uint256(100)
        assert isinstance(value, Uint256)
        assert value.to_int() == 100
        
        # Convert string to Uint256
        value = to_uint256("100")
        assert isinstance(value, Uint256)
        assert value.to_int() == 100
        
        # Error for invalid values
        with pytest.raises(ValueError):
            to_uint256(-1)
        
        with pytest.raises(ValueError):
            to_uint256(2**256)

        # Error for invalid type
        with pytest.raises(TypeError):
            to_uint256(1.5)
    
    def test_remove_decimals(self):
        # Test with integer value
        value = remove_decimals(1)
        assert isinstance(value, Uint256)
        assert value.to_int() == 10**18
        
        # Test with decimal value
        value = remove_decimals(0.01)
        assert isinstance(value, Uint256)
        assert value.to_int() == 10**16
        
        # Test with Decimal type
        value = remove_decimals(Decimal('0.01'))
        assert isinstance(value, Uint256)
        assert value.to_int() == 10**16
        
        # Test with large value
        value = remove_decimals(100)
        assert isinstance(value, Uint256)
        assert value.to_int() == 100 * 10**18
    
    def test_restore_decimals(self):
        # Convert from Uint256
        uint_value = Uint256(10**18)
        value = restore_decimals(uint_value)
        assert value == 1.0
        
        # Convert from integer
        value = restore_decimals(10**18)
        assert value == 1.0
        
        # Test with small value
        uint_value = Uint256(10**16)
        value = restore_decimals(uint_value)
        assert value == 0.01
        
        # Test with large value
        uint_value = Uint256(100 * 10**18)
        value = restore_decimals(uint_value)
        assert value == 100.0
    
    def test_round_trip(self):
        # Convert integer value and restore
        original = 100
        uint_value = remove_decimals(original)
        restored = restore_decimals(uint_value)
        assert restored == original
        
        # Convert decimal value and restore
        original = 0.01
        uint_value = remove_decimals(original)
        restored = restore_decimals(uint_value)
        assert restored == original
        
        # Convert Decimal value and restore
        original = Decimal('0.01')
        uint_value = remove_decimals(original)
        restored = restore_decimals(uint_value)
        assert float(original) == restored 