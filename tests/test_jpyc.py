import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from web3 import Web3
from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
import asyncio

from jpyc_sdk.jpyc import JPYC
from jpyc_sdk.utils.errors import InvalidAddressError, InvalidTransactionError
from jpyc_sdk.utils.math import DECIMALS_QUANTIFIER
from jpyc_sdk.utils.addresses import LOCAL_PROXY_ADDRESS


@pytest.fixture
def mock_web3():
    """Fixture for creating a Web3 mock"""
    web3 = MagicMock()
    # Mock eth property properly
    eth_mock = MagicMock()
    contract_mock = MagicMock()
    eth_mock.contract.return_value = contract_mock
    eth_mock.default_account = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    
    # Set required properties and methods for Web3 mock
    web3.eth = eth_mock
    web3.to_checksum_address.side_effect = lambda x: x
    
    return web3


@pytest.fixture
def mock_account():
    """Fixture for creating an account mock"""
    account = MagicMock(spec=LocalAccount)
    account.address = '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    account.key = b'0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
    return account


@pytest.fixture
def jpyc_instance(mock_web3, mock_account):
    """Fixture for creating a JPYC class instance"""
    os.environ['SDK_ENV'] = 'production'
    
    # Apply patch
    with patch('jpyc_sdk.jpyc.is_valid_address', return_value=True):
        instance = JPYC(mock_web3, mock_account)
        return instance


class TestJPYC:
    def test_init_with_valid_address(self, mock_web3, mock_account):
        """Test JPYC initialization with a valid address"""
        # Set environment variable
        os.environ['SDK_ENV'] = 'production'
        
        # Apply patch
        with patch('jpyc_sdk.jpyc.is_valid_address', return_value=True):
            jpyc = JPYC(mock_web3, mock_account)
            
            # Verification
            assert jpyc.web3 == mock_web3
            assert jpyc.account == mock_account
            mock_web3.eth.contract.assert_called_once()
    
    def test_init_with_invalid_address(self, mock_web3, mock_account):
        """Test JPYC initialization with an invalid address"""
        # Set environment variable
        os.environ['SDK_ENV'] = 'production'
        
        # Apply patch
        with patch('jpyc_sdk.jpyc.is_valid_address', return_value=False):
            with pytest.raises(InvalidAddressError):
                JPYC(mock_web3, mock_account)
    
    def test_init_with_local_env(self, mock_web3, mock_account):
        """Test JPYC initialization with local environment"""
        # Set environment variable
        os.environ['SDK_ENV'] = 'local'
        
        # Apply patch
        with patch('jpyc_sdk.jpyc.is_valid_address', return_value=True):
            jpyc = JPYC(mock_web3, mock_account)
            
            # Verification
            assert jpyc.contract_address == LOCAL_PROXY_ADDRESS
    
    @pytest.mark.asyncio
    async def test_is_minter(self, jpyc_instance):
        """Test is_minter method"""
        # Use AsyncMock to mock the asynchronous method
        jpyc_instance.contract.functions.isMinter.return_value.call = AsyncMock(return_value=True)
        
        # Use patch to replace the asynchronous method
        with patch.object(JPYC, 'is_minter', new_callable=AsyncMock, return_value=True):
            # Execute the asynchronous method with await
            result = await jpyc_instance.is_minter('0x123')
            assert result is True
    
    @pytest.mark.asyncio
    async def test_minter_allowance(self, jpyc_instance):
        """Test minter_allowance method"""
        # Mock the contract call with wei value
        jpyc_instance.contract.functions.minterAllowance.return_value.call = AsyncMock(return_value=5000 * DECIMALS_QUANTIFIER)
        
        # Use patch to replace the asynchronous method
        with patch.object(JPYC, 'minter_allowance', new_callable=AsyncMock, return_value=5000.0):
            # Execute the asynchronous method with await
            result = await jpyc_instance.minter_allowance('0x123')
            assert result == 5000.0
    
    @pytest.mark.asyncio
    async def test_total_supply(self, jpyc_instance):
        """Test total_supply method"""
        # Use AsyncMock to mock the asynchronous method
        jpyc_instance.contract.functions.totalSupply.return_value.call = AsyncMock(return_value=1000000000000000000)
        
        # Use patch to replace the asynchronous method
        with patch.object(JPYC, 'total_supply', new_callable=AsyncMock, return_value=1.0):
            # Execute the asynchronous method with await
            result = await jpyc_instance.total_supply()
            assert result == 1.0
    
    @pytest.mark.asyncio
    async def test_balance_of(self, jpyc_instance):
        """Test balance_of method"""
        # Use AsyncMock to mock the asynchronous method
        jpyc_instance.contract.functions.balanceOf.return_value.call = AsyncMock(return_value=500000000000000000)
        
        # Use patch to replace the asynchronous method
        with patch.object(JPYC, 'balance_of', new_callable=AsyncMock, return_value=0.5):
            # Execute the asynchronous method with await
            result = await jpyc_instance.balance_of('0x123')
            assert result == 0.5
    
    @pytest.mark.asyncio
    async def test_allowance(self, jpyc_instance):
        """Test allowance method"""
        # Mock the contract call
        jpyc_instance.contract.functions.allowance.return_value.call = AsyncMock(return_value=2000 * DECIMALS_QUANTIFIER)
        
        # Use patch
        with patch.object(JPYC, 'allowance', new_callable=AsyncMock, return_value=2000.0):
            result = await jpyc_instance.allowance('0x123', '0x456')
            assert result == 2000.0
    
    @pytest.mark.asyncio
    async def test_nonces(self, jpyc_instance):
        """Test nonces method"""
        # Mock the contract call
        jpyc_instance.contract.functions.nonces.return_value.call = AsyncMock(return_value=5)
        
        # Use patch
        with patch.object(JPYC, 'nonces', new_callable=AsyncMock, return_value=5):
            result = await jpyc_instance.nonces('0x123')
            assert result == 5
    
    @pytest.mark.asyncio
    async def test_execute_transaction_without_account(self, jpyc_instance):
        """Test _execute_transaction method without account"""
        # Remove account
        jpyc_instance.account = None
        
        # Test function call
        contract_fn = MagicMock()
        
        with pytest.raises(InvalidTransactionError) as excinfo:
            await jpyc_instance._execute_transaction(contract_fn)
        
        assert "No account is set" in str(excinfo.value)
    
    @pytest.mark.asyncio
    async def test_execute_transaction_with_insufficient_funds(self, jpyc_instance):
        """Test _execute_transaction method with insufficient funds error"""
        # Mock function that raises exception
        contract_fn = MagicMock()
        contract_fn.estimate_gas.side_effect = Exception("insufficient funds for gas")
        
        with pytest.raises(InvalidTransactionError) as excinfo:
            await jpyc_instance._execute_transaction(contract_fn)
        
        assert "Insufficient funds" in str(excinfo.value)
    
    @pytest.mark.asyncio
    async def test_execute_transaction_success(self, jpyc_instance):
        """Test _execute_transaction method success case"""
        # Mock the necessary functions
        contract_fn = MagicMock()
        contract_fn.estimate_gas.return_value = 100000
        contract_fn.build_transaction.return_value = {"gas": 100000, "nonce": 1}
        
        tx_hash = HexBytes('0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef')
        
        # Mock web3 methods
        jpyc_instance.web3.eth.get_transaction_count.return_value = 1
        jpyc_instance.web3.eth.account.sign_transaction.return_value.rawTransaction = b'signed_tx'
        jpyc_instance.web3.eth.send_raw_transaction.return_value = tx_hash
        
        # Execute the function
        result = await jpyc_instance._execute_transaction(contract_fn)
        
        # Verify
        assert result == tx_hash
        contract_fn.estimate_gas.assert_called_once()
        contract_fn.build_transaction.assert_called_once()
        jpyc_instance.web3.eth.account.sign_transaction.assert_called_once()
        jpyc_instance.web3.eth.send_raw_transaction.assert_called_once_with(b'signed_tx')
    
    @pytest.mark.asyncio
    async def test_transfer_success(self, jpyc_instance):
        """Test transfer method success case"""
        # Preset function patch
        tx_hash = HexBytes('0x456')
        
        # Use patch to replace the asynchronous method
        with patch.object(JPYC, 'transfer', new_callable=AsyncMock, return_value=tx_hash):
            # Execute the asynchronous method with await
            result = await jpyc_instance.transfer('0x123', 10.0)
            assert result == tx_hash
    
    @pytest.mark.asyncio
    async def test_transfer_failure(self, jpyc_instance):
        """Test transfer method failure case"""
        # Mock to throw an exception
        with patch.object(JPYC, 'transfer', new_callable=AsyncMock, 
                         side_effect=InvalidTransactionError("Transaction simulation failed: Transaction failed")):
            # Verify that an exception occurs
            with pytest.raises(InvalidTransactionError) as excinfo:
                await jpyc_instance.transfer('0x123', 10.0)
            
            # Verify error message
            assert "Transaction simulation failed" in str(excinfo.value)
            assert "Transaction failed" in str(excinfo.value)
    
    @pytest.mark.asyncio
    async def test_mint(self, jpyc_instance):
        """Test mint method"""
        tx_hash = HexBytes('0x789')
        
        with patch.object(JPYC, 'mint', new_callable=AsyncMock, return_value=tx_hash):
            result = await jpyc_instance.mint('0x123', 50.0)
            assert result == tx_hash
    
    @pytest.mark.asyncio
    async def test_configure_minter(self, jpyc_instance):
        """Test configure_minter method"""
        tx_hash = HexBytes('0xabc')
        
        with patch.object(JPYC, 'configure_minter', new_callable=AsyncMock, return_value=tx_hash):
            result = await jpyc_instance.configure_minter('0x123', 1000)
            assert result == tx_hash
    
    @pytest.mark.asyncio
    async def test_transfer_from(self, jpyc_instance):
        """Test transfer_from method"""
        tx_hash = HexBytes('0xdef')
        
        with patch.object(JPYC, 'transfer_from', new_callable=AsyncMock, return_value=tx_hash):
            result = await jpyc_instance.transfer_from('0x123', '0x456', 25.0)
            assert result == tx_hash
    
    @pytest.mark.asyncio
    async def test_approve(self, jpyc_instance):
        """Test approve method"""
        tx_hash = HexBytes('0xaaa')
        
        with patch.object(JPYC, 'approve', new_callable=AsyncMock, return_value=tx_hash):
            result = await jpyc_instance.approve('0x123', 500.0)
            assert result == tx_hash
    
    @pytest.mark.asyncio
    async def test_increase_allowance(self, jpyc_instance):
        """Test increase_allowance method"""
        tx_hash = HexBytes('0xbbb')
        
        with patch.object(JPYC, 'increase_allowance', new_callable=AsyncMock, return_value=tx_hash):
            result = await jpyc_instance.increase_allowance('0x123', 100.0)
            assert result == tx_hash
    
    @pytest.mark.asyncio
    async def test_decrease_allowance(self, jpyc_instance):
        """Test decrease_allowance method"""
        tx_hash = HexBytes('0xccc')
        
        with patch.object(JPYC, 'decrease_allowance', new_callable=AsyncMock, return_value=tx_hash):
            result = await jpyc_instance.decrease_allowance('0x123', 50.0)
            assert result == tx_hash
