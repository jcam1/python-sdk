from eth_account.signers.local import LocalAccount
from pydantic import ValidationError
import pytest
from web3 import Web3

from packages.core.jpyc_core_sdk.client import SdkClient
from packages.core.jpyc_core_sdk.utils.chains import get_default_rpc_endpoint
from packages.core.jpyc_core_sdk.utils.errors import (
    AccountNotInitialized,
    InvalidBytes32,
    InvalidRpcEndpoint,
    NetworkNotSupported,
)

from .conftest import KNOWN_ACCOUNTS


@pytest.mark.parametrize(
    [
        "chain_name",
        "network_name",
        "rpc_endpoint",
        "private_key",
        "num_of_middlewares",
        "address",
    ],
    [
        pytest.param(
            "ethereum",
            "mainnet",
            None,
            None,
            6,
            None,
            id="valid default network; without account",
        ),
        pytest.param(
            "ethereum",
            "mainnet",
            "http://127.0.0.1:8545/",
            None,
            6,
            None,
            id="valid custom network; without account",
        ),
        pytest.param(
            "ethereum",
            "mainnet",
            None,
            KNOWN_ACCOUNTS[0].private_key,
            7,
            KNOWN_ACCOUNTS[0].address,
            id="valid network; with account",
        ),
    ],
)
def test_constructor(
    chain_name,
    network_name,
    rpc_endpoint,
    private_key,
    num_of_middlewares,
    address,
):
    client = SdkClient(
        chain_name=chain_name,
        network_name=network_name,
        rpc_endpoint=rpc_endpoint,
        private_key=private_key,
    )

    assert isinstance(client.w3, Web3)
    assert len(client.w3.middleware_onion.middleware) == num_of_middlewares
    assert client.rpc_endpoint == (
        get_default_rpc_endpoint(chain_name, network_name)
        if rpc_endpoint is None
        else rpc_endpoint
    )
    if private_key is None:
        assert client.account is None
    else:
        assert isinstance(client.account, LocalAccount)
        assert client.account.address == address
        assert client.w3.eth.default_account == address


@pytest.mark.parametrize(
    [
        "chain_name",
        "network_name",
        "rpc_endpoint",
        "private_key",
        "exception_class",
    ],
    [
        pytest.param(
            "solana",
            "mainnet",
            None,
            None,
            ValidationError,
            id="invalid chain_name",
        ),
        pytest.param(
            "localhost",
            "mainnet",
            None,
            None,
            NetworkNotSupported,
            id="invalid network configuration",
        ),
        pytest.param(
            "ethereum",
            "mainnet",
            "invalid_uri",
            None,
            InvalidRpcEndpoint,
            id="invalid rpc_endpoint",
        ),
        pytest.param(
            "ethereum",
            "mainnet",
            None,
            "invalid_private_key",
            InvalidBytes32,
            id="invalid private_key",
        ),
    ],
)
def test_constructor_failures(
    chain_name,
    network_name,
    rpc_endpoint,
    private_key,
    exception_class,
):
    with pytest.raises(exception_class):
        SdkClient(
            chain_name=chain_name,
            network_name=network_name,
            rpc_endpoint=rpc_endpoint,
            private_key=private_key,
        )


def test_set_default_provider(sdk_client):
    sdk_client.set_default_provider(
        chain_name="ethereum",
        network_name="sepolia",
    )

    assert (
        sdk_client.w3.provider.endpoint_uri
        == "https://ethereum-sepolia-rpc.publicnode.com"
    )
    assert sdk_client.w3.eth.default_account == KNOWN_ACCOUNTS[0].address


@pytest.mark.parametrize(
    [
        "chain_name",
        "network_name",
        "exception_class",
    ],
    [
        pytest.param(
            "solana",
            "mainnet",
            ValidationError,
            id="invalid chain_name",
        ),
        pytest.param(
            "localhost",
            "mainnet",
            NetworkNotSupported,
            id="invalid network configuration",
        ),
    ],
)
def test_set_default_provider_failures(
    sdk_client,
    chain_name,
    network_name,
    exception_class,
):
    with pytest.raises(exception_class):
        sdk_client.set_default_provider(
            chain_name=chain_name,
            network_name=network_name,
        )


def test_set_custom_provider(sdk_client):
    rpc_endpoint = "https://astar.public.blastapi.io"

    sdk_client.set_custom_provider(
        rpc_endpoint=rpc_endpoint,
    )

    assert sdk_client.w3.provider.endpoint_uri == rpc_endpoint
    assert sdk_client.w3.eth.default_account == KNOWN_ACCOUNTS[0].address


def test_set_custom_provider_failures(sdk_client):
    with pytest.raises(InvalidRpcEndpoint):
        sdk_client.set_custom_provider(
            rpc_endpoint="invalid_uri",
        )


@pytest.mark.parametrize(
    [
        "private_key",
        "address",
    ],
    [
        pytest.param(
            KNOWN_ACCOUNTS[1].private_key,
            KNOWN_ACCOUNTS[1].address,
            id="set new account to account",
        ),
        pytest.param(
            None,
            None,
            id="set None to account",
        ),
    ],
)
def test_set_account(
    sdk_client,
    private_key,
    address,
):
    account = sdk_client.set_account(
        private_key=private_key,
    )

    assert sdk_client.w3.provider.endpoint_uri == "https://ethereum-rpc.publicnode.com"

    if account is not None:
        assert account.address == address
        assert sdk_client.w3.eth.default_account == address
    else:
        assert account is None
        assert sdk_client.w3.eth.default_account is None


def test_set_account_failures(sdk_client):
    with pytest.raises(InvalidBytes32):
        sdk_client.set_account(
            private_key="invalid_private_key",
        )


def test_get_account_address(sdk_client):
    address = sdk_client.get_account_address()

    assert address == KNOWN_ACCOUNTS[0].address


def test_get_account_address_failures(sdk_client_without_account):
    with pytest.raises(AccountNotInitialized):
        sdk_client_without_account.get_account_address()
