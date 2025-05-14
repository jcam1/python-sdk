from eth_account.signers.local import LocalAccount
from web3 import Account, HTTPProvider, Web3
from web3.middleware import ExtraDataToPOAMiddleware, SignAndSendRawMiddlewareBuilder

from interfaces import ISdkClient
from utils import get_default_rpc_endpoint

class SdkClient(ISdkClient):
    """SDK client.

    Attributes:
        w3 (Web3): Configured web3 instance
        account (LocalAccount): Local account
    """
    w3: Web3
    account: LocalAccount

    def __init__(
        self,
        chain_name: str,
        network_name: str,
        private_key: str,
    ):
        """Constructor that initializes SDK client.

        Args:
            chain_name (str): Chain name
            network_name (str): Network name
            private_key (str): private key of EOA

        Raises:
            NetworkNotSupported: If the specified network is not supported by the SDK
        """
        rpc_endpoint = get_default_rpc_endpoint(chain_name, network_name)
        account = Account.from_key(private_key)

        w3 = Web3(HTTPProvider(rpc_endpoint))
        w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(account), layer=0)

        self.w3 = w3
        self.account = account

    def set_default_provider(self, chain_name: str, network_name: str) -> Web3:
        rpc_endpoint = get_default_rpc_endpoint(chain_name, network_name)

        self.w3 = Web3(HTTPProvider(rpc_endpoint))

        return self.w3

    def set_custom_provider(self, rpc_endpoint: str) -> Web3:
        self.w3 = Web3(HTTPProvider(rpc_endpoint))

        return self.w3

    def set_account(self, private_key: str) -> LocalAccount:
        account = Account.from_key(private_key)
        self.w3.middleware_onion.replace(SignAndSendRawMiddlewareBuilder.build(self.account), SignAndSendRawMiddlewareBuilder.build(account))
        self.account = account

        return self.account

    def get_account_address(self) -> str:
        return self.account.address
