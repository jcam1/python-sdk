import os
from typing import Optional, Union
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import SignAndSendRawMiddlewareBuilder

from .interfaces.client import ISdkClient
from .utils.types import Address, ChainName, NetworkName, Endpoint
from .utils.chains import get_web3_for_chain, is_valid_chain_name, is_valid_network_name
from .utils.errors import InvalidChainNameError, InvalidNetworkNameError

class SdkClient(ISdkClient):
    """SDK client for interacting with JPYC tokens"""
    
    def __init__(self, chain_name: ChainName, network_name: NetworkName, rpc_endpoint: Endpoint):
        """
        Initialize the SDK client.
        
        Args:
            chain_name: Chain name (e.g., 'ethereum', 'polygon')
            network_name: Network name (e.g., 'mainnet', 'goerli')
            rpc_endpoint: RPC endpoint URL
            
        Raises:
            InvalidChainNameError: If the chain name is not supported
            InvalidNetworkNameError: If the network name is not supported for the chain
        """
        if not is_valid_chain_name(chain_name):
            raise InvalidChainNameError(chain_name)
        if not is_valid_network_name(chain_name, network_name):
            raise InvalidNetworkNameError(chain_name, network_name)
        
        self.chain_name = chain_name
        self.network_name = network_name
        self.rpc_endpoint = rpc_endpoint
        self.web3 = get_web3_for_chain(chain_name, network_name, rpc_endpoint)
        self.account = None
    
    def create_private_key_account(self, private_key: Optional[str] = None) -> Optional[LocalAccount]:
        """
        Create an account from a private key.
        
        Args:
            private_key: Private key (optional, will use environment variable if not specified)
            
        Returns:
            LocalAccount: Account created from the private key
            
        Raises:
            ValueError: If no private key is provided and none is found in environment variables
        """
        pk = private_key or os.environ.get('PRIVATE_KEY')
        if not pk:
            raise ValueError("Private key not provided and not found in environment variables")
        
        self.account = Account.from_key(pk)
        return self.account
    
    def create_local_client(self, account: Optional[Union[str, LocalAccount]] = None) -> Web3:
        """
        Create a client from an account.
        
        Args:
            account: Account to use (optional, will use the account created with create_private_key_account if not specified)
            
        Returns:
            Web3: Web3 instance configured with the account
            
        Raises:
            ValueError: If no account is provided and no account has been created with create_private_key_account
        """
        if account is None:
            if self.account is None:
                raise ValueError("No account provided and no account created with create_private_key_account")
            account = self.account
        
        if self.web3 is None:
            self.web3 = Web3(Web3.HTTPProvider(self.rpc_endpoint))
        
        if isinstance(account, str):
            # Treat as address and use
            self.web3.eth.default_account = Web3.to_checksum_address(account)
        else:
            # Set up middleware for account
            self.web3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(account), layer=0)
            self.web3.eth.default_account = account.address
        
        return self.web3