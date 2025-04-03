import pytest
from jpyc_sdk.utils.types import Uint256, Uint8

class TestUint256:
    def test_init_with_valid_values(self):
        # Test with positive integer
        value = Uint256(100)
        assert value.to_int() == 100
        assert str(value) == "100"
        assert repr(value) == "Uint256(100)"
        
        # Test with zero
        value = Uint256(0)
        assert value.to_int() == 0
        
        # Test with maximum value (2^256-1)
        max_value = 2**256 - 1
        value = Uint256(max_value)
        assert value.to_int() == max_value
    
    def test_init_with_invalid_values(self):
        # Test with negative number
        with pytest.raises(ValueError) as excinfo:
            Uint256(-1)
        assert "outside the range of uint256" in str(excinfo.value)
        
        # Test with out-of-range value
        with pytest.raises(ValueError) as excinfo:
            Uint256(2**256)
        assert "outside the range of uint256" in str(excinfo.value)
        
        # Test with non-integer value
        with pytest.raises(TypeError) as excinfo:
            Uint256("100")
        assert "Expected int" in str(excinfo.value)
    
    def test_from_string(self):
        # Test with valid string
        value = Uint256.from_string("100")
        assert value.to_int() == 100
        
        # Test with invalid string
        with pytest.raises(ValueError) as excinfo:
            Uint256.from_string("not a number")
        assert "Cannot convert" in str(excinfo.value)
    
    def test_from_value(self):
        # Test with integer
        value = Uint256.from_value(100)
        assert value.to_int() == 100
        
        # Test with string
        value = Uint256.from_value("100")
        assert value.to_int() == 100
        
        # Test with invalid type
        with pytest.raises(TypeError) as excinfo:
            Uint256.from_value(1.5)
        assert "Expected int or str" in str(excinfo.value)
    
    def test_comparison(self):
        a = Uint256(100)
        b = Uint256(100)
        c = Uint256(200)
        
        assert a == b
        assert a == 100
        assert a != c
        assert a != 200

class TestUint8:
    def test_init_with_valid_values(self):
        # Test with positive integer
        value = Uint8(123)
        assert value.to_int() == 123
        assert repr(value) == "Uint8(123)"
        
        # Test with zero
        value = Uint8(0)
        assert value.to_int() == 0
        
        # Test with maximum value (255)
        value = Uint8(255)
        assert value.to_int() == 255
    
    def test_init_with_invalid_values(self):
        # Test with negative number
        with pytest.raises(ValueError) as excinfo:
            Uint8(-1)
        assert "outside the range of uint8" in str(excinfo.value)
        
        # Test with out-of-range value
        with pytest.raises(ValueError) as excinfo:
            Uint8(256)
        assert "outside the range of uint8" in str(excinfo.value)
        
        # Test with non-integer value
        with pytest.raises(TypeError) as excinfo:
            Uint8("100")
        assert "Expected int" in str(excinfo.value)
    
    def test_comparison(self):
        a = Uint8(123)
        b = Uint8(123)
        c = Uint8(200)
        
        assert a == b
        assert a == 123
        assert a != c
        assert a != 200 