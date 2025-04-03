"""
Tests for SdkClient implementation
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider
from eth_account import Account

from jpyc_sdk.client import SdkClient
from jpyc_sdk.utils.errors import InvalidChainNameError, InvalidNetworkNameError

# Test fixtures
@pytest.fixture
def eth_tester_provider():
    return EthereumTesterProvider()

@pytest.fixture
def web3(eth_tester_provider):
    return Web3(eth_tester_provider)

@pytest.fixture
def valid_chain_name():
    return "ethereum"

@pytest.fixture
def valid_network_name():
    return "mainnet"

@pytest.fixture
def valid_rpc_endpoint():
    return "https://ethereum.publicnode.com"

@pytest.fixture
def sdk_client(valid_chain_name, valid_network_name, valid_rpc_endpoint):
    with patch('jpyc_sdk.client.get_web3_for_chain') as mock_get_web3:
        mock_web3 = MagicMock()
        mock_get_web3.return_value = mock_web3
        client = SdkClient(valid_chain_name, valid_network_name, valid_rpc_endpoint)
        return client

# Tests for SdkClient.__init__
def test_init_with_valid_inputs(valid_chain_name, valid_network_name, valid_rpc_endpoint):
    """Test initialization with valid inputs"""
    with patch('jpyc_sdk.client.get_web3_for_chain') as mock_get_web3:
        mock_web3 = MagicMock()
        mock_get_web3.return_value = mock_web3
        
        client = SdkClient(valid_chain_name, valid_network_name, valid_rpc_endpoint)
        
        assert client.chain_name == valid_chain_name
        assert client.network_name == valid_network_name
        assert client.rpc_endpoint == valid_rpc_endpoint
        assert client.web3 == mock_web3
        assert client.account is None

def test_init_with_invalid_chain_name(valid_network_name, valid_rpc_endpoint):
    """Test initialization with invalid chain name"""
    with pytest.raises(InvalidChainNameError):
        SdkClient("invalid_chain", valid_network_name, valid_rpc_endpoint)

def test_init_with_invalid_network_name(valid_chain_name, valid_rpc_endpoint):
    """Test initialization with invalid network name"""
    with pytest.raises(InvalidNetworkNameError):
        SdkClient(valid_chain_name, "invalid_network", valid_rpc_endpoint)

# Tests for SdkClient.create_private_key_account
def test_create_private_key_account_with_explicit_private_key(sdk_client):
    """Test creating an account with an explicitly provided private key"""
    private_key = "0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    
    with patch('jpyc_sdk.client.Account.from_key') as mock_from_key:
        mock_account = MagicMock()
        mock_from_key.return_value = mock_account
        
        account = sdk_client.create_private_key_account(private_key)
        
        mock_from_key.assert_called_once_with(private_key)
        assert account == mock_account
        assert sdk_client.account == mock_account

def test_create_private_key_account_with_env_variable(sdk_client):
    """Test creating an account with a private key from environment variable"""
    private_key = "0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    
    with patch.dict(os.environ, {"PRIVATE_KEY": private_key}):
        with patch('jpyc_sdk.client.Account.from_key') as mock_from_key:
            mock_account = MagicMock()
            mock_from_key.return_value = mock_account
            
            account = sdk_client.create_private_key_account()
            
            mock_from_key.assert_called_once_with(private_key)
            assert account == mock_account
            assert sdk_client.account == mock_account

def test_create_private_key_account_with_no_private_key(sdk_client):
    """Test creating an account with no private key provided"""
    with patch.dict(os.environ, {}, clear=True):  # Clear environment variables
        with pytest.raises(ValueError) as excinfo:
            sdk_client.create_private_key_account()
        
        assert "Private key not provided" in str(excinfo.value)

# Tests for SdkClient.create_local_client
def test_create_local_client_with_explicit_account(sdk_client):
    """Test creating a local client with an explicitly provided account"""
    mock_account = MagicMock()
    mock_account.address = "0x1234567890123456789012345678901234567890"
    
    result = sdk_client.create_local_client(mock_account)
    
    # Check middleware was added
    sdk_client.web3.middleware_onion.inject.assert_called_once()
    assert sdk_client.web3.eth.default_account == mock_account.address
    assert result == sdk_client.web3

def test_create_local_client_with_previously_created_account(sdk_client):
    """Test creating a local client with a previously created account"""
    mock_account = MagicMock()
    mock_account.address = "0x1234567890123456789012345678901234567890"
    sdk_client.account = mock_account
    
    result = sdk_client.create_local_client()
    
    # Check middleware was added
    sdk_client.web3.middleware_onion.inject.assert_called_once()
    assert sdk_client.web3.eth.default_account == mock_account.address
    assert result == sdk_client.web3

def test_create_local_client_with_address_string(sdk_client):
    """Test creating a local client with an address string"""
    address = "0x1234567890123456789012345678901234567890"
    
    with patch('jpyc_sdk.client.Web3.to_checksum_address') as mock_to_checksum:
        mock_to_checksum.return_value = address
        
        result = sdk_client.create_local_client(address)
        
        mock_to_checksum.assert_called_once_with(address)
        assert sdk_client.web3.eth.default_account == address
        assert result == sdk_client.web3

def test_create_local_client_with_no_account(sdk_client):
    """Test creating a local client with no account provided"""
    with pytest.raises(ValueError) as excinfo:
        sdk_client.create_local_client()
    
    assert "No account provided" in str(excinfo.value)

def test_create_local_client_with_missing_web3(sdk_client):
    """Test creating a local client when web3 instance is missing"""
    sdk_client.web3 = None
    mock_account = MagicMock()
    mock_account.address = "0x1234567890123456789012345678901234567890"
    sdk_client.account = mock_account
    
    with patch('jpyc_sdk.client.Web3') as mock_web3_class:
        mock_web3 = MagicMock()
        mock_web3_class.HTTPProvider.return_value = MagicMock()
        mock_web3_class.return_value = mock_web3
        
        result = sdk_client.create_local_client()
        
        mock_web3_class.HTTPProvider.assert_called_once_with(sdk_client.rpc_endpoint)
        mock_web3_class.assert_called_once()
        assert sdk_client.web3 == mock_web3
        assert result == mock_web3