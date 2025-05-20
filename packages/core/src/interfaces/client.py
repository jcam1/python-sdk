from abc import ABC, abstractmethod

from eth_account.signers.local import LocalAccount
from web3 import Web3

from ..utils.types import ChainName
from ..utils.validators import (
    Bytes32,
    ChecksumAddress,
    RpcEndpoint,
)


class ISdkClient(ABC):
    """Interface of SDK client."""

    @abstractmethod
    def set_default_provider(self, chain_name: ChainName, network_name: str) -> Web3:
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
    def set_custom_provider(self, rpc_endpoint: RpcEndpoint) -> Web3:
        """Set provider using a custom RPC endpoint.

        Args:
            rpc_endpoint (RpcEndpoint): Custom RPC endpoint

        Returns:
            Web3: Configured web3 instance

        Raises:
            InvalidRpcEndpoint: If the supplied `rpc_endpoint` is not in a valid form
        """
        pass

    @abstractmethod
    def set_account(self, private_key: Bytes32 | None) -> LocalAccount | None:
        """Set account with a private key.

        Notes:
            If `private_key` parameter is set to `None`, \
            this method removes `account` from the configured web3 instance.

        Args:
            private_key (Bytes32, optional): Private key of account

        Returns:
            LocalAccount | None: Configured account instance

        Raises:
            InvalidBytes32: If the supplied `private_key` is not in a valid form
        """
        pass

    @abstractmethod
    def get_account_address(self) -> ChecksumAddress:
        """Get address of the configured account.

        Returns:
            ChecksumAddress: Public address of account

        Raises:
            AccountNotInitialized: If account is not initialized
        """
        pass
