"""
Interface definitions for the SDK client
"""

from typing import Protocol, Optional, Any
from eth_account.signers.local import LocalAccount
from web3 import Web3

class ISdkClient(Protocol):
    """
    Interface for the SDK client
    
    This interface defines the methods required for SDK client operations.
    """
    
    def create_private_key_account(self, private_key: Optional[str] = None) -> Optional[LocalAccount]:
        """
        Create an account from a private key
        
        Args:
            private_key: Private key (optional)
            
        Returns:
            LocalAccount: Created account
        """
        ...
    
    def create_local_client(self, account: Optional[Any] = None) -> Web3:
        """
        Create a local client configured with an account
        
        Args:
            account: Account to use (optional)
            
        Returns:
            Web3: Configured Web3 instance
        """
        ...