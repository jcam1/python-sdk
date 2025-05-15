from abc import ABC, abstractmethod

from eth_account.signers.local import LocalAccount
from web3 import Web3

class ISdkClient(ABC):
    """Interface of SDK client."""

    @abstractmethod
    def set_default_provider(self, chain_name: str, network_name: str) -> Web3:
        """Set provider using one of the default RPC endpoints.

        Args:
            chain_name (str): Chain name
            network_name (str): Network name

        Returns:
            Web3: Configured web3 instance

        Raises:
            NetworkNotSupported: If the specified network is not supported by the SDK
        """
        pass

    @abstractmethod
    def set_custom_provider(self, rpc_endpoint: str) -> Web3:
        """Set provider using a custom RPC endpoint.

        Args:
            rpc_endpoint (str): Custom RPC endpoint

        Returns:
            Web3: Configured web3 instance
        """
        pass

    @abstractmethod
    def set_account(self, private_key: str) -> LocalAccount:
        """Set account with private key.

        Args:
            private_key (str): Private key of account

        Returns:
            LocalAccount: Configured account
        """
        pass

    @abstractmethod
    def get_account_address(self) -> str:
        """Get address of the configured account.

        Returns:
            str: Public address of account

        Raises:
            AccountNotInitialized: If account is not initialized
        """
        pass
