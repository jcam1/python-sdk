from eth_account.signers.local import LocalAccount
from web3 import Account, HTTPProvider, Web3
from web3.middleware import ExtraDataToPOAMiddleware, SignAndSendRawMiddlewareBuilder

from interfaces import ISdkClient
from utils.chains import (
    get_default_rpc_endpoint,
)
from utils.constants import (
    POA_MIDDLEWARE,
    SIGN_MIDDLEWARE,
)
from utils.errors import AccountNotInitialized

class SdkClient(ISdkClient):
    """SDK client."""

    def __init__(
        self,
        chain_name: str,
        network_name: str,
        private_key: str | None = None,
    ):
        """Constructor that initializes SDK client.

        Args:
            chain_name (str): Chain name
            network_name (str): Network name
            private_key (str | None): private key of EOA

        Raises:
            NetworkNotSupported: If the specified network is not supported by the SDK
        """
        rpc_endpoint = get_default_rpc_endpoint(chain_name, network_name)
        account = Account.from_key(private_key) if private_key is not None else None
        w3 = self.__configure_w3(
            rpc_endpoint=rpc_endpoint,
            account=account,
        )

        self.w3 = w3
        """Web3: Configured web3 instance"""
        self.rpc_endpoint = rpc_endpoint
        """str: RPC endpoint"""
        self.account = account
        """LocalAccount | None: Account instance"""

    def __configure_w3(
            self,
            rpc_endpoint: str,
            account: LocalAccount | None = None,
        ) -> Web3:
        """Configure a web3 instance.

        Args:
            rpc_endpoint (str): RPC endpoint
            account (LocalAccount | None): Account instance

        Returns:
            Web3: Configured web3 instance
        """
        w3 = Web3(HTTPProvider(rpc_endpoint))
        w3.middleware_onion.inject(
            ExtraDataToPOAMiddleware,
            name=POA_MIDDLEWARE,
            layer=0,
        )
        if account is not None:
            w3.middleware_onion.inject(
                SignAndSendRawMiddlewareBuilder.build(account),
                name=SIGN_MIDDLEWARE,
                layer=0,
            )

        return w3

    def set_default_provider(self, chain_name: str, network_name: str) -> Web3:
        self.w3 = self.__configure_w3(
            rpc_endpoint=get_default_rpc_endpoint(chain_name, network_name),
            account=self.account
        )

        return self.w3

    def set_custom_provider(self, rpc_endpoint: str) -> Web3:
        self.w3 = self.__configure_w3(
            rpc_endpoint=rpc_endpoint,
            account=self.account
        )

        return self.w3

    def set_account(self, private_key: str) -> LocalAccount:
        self.account = Account.from_key(private_key)
        self.w3 = self.__configure_w3(
            rpc_endpoint=self.rpc_endpoint,
            account=self.account
        )

        return self.account

    def get_account_address(self) -> str:
        if self.account is None:
            raise AccountNotInitialized()

        return self.account.address
