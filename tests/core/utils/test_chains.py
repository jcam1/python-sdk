import pytest

from packages.core.src.utils.chains import (
    enumerate_supported_networks,
    get_default_rpc_endpoint,
    is_supported_network,
)
from packages.core.src.utils.errors import (
    NetworkNotSupported,
)


def test_enumerate_supported_networks():
    supported_networks = enumerate_supported_networks()
    assert (
        supported_networks == "'ethereum' => ['mainnet', 'sepolia'], "
        "'polygon' => ['mainnet', 'amoy'], "
        "'gnosis' => ['mainnet', 'chiado'], "
        "'avalanche' => ['mainnet', 'fuji'], "
        "'astar' => ['mainnet'], "
        "'shiden' => ['mainnet'], "
        "'localhost' => ['devnet']"
    )


@pytest.mark.parametrize(
    ["chain_name", "network_name", "response"],
    [
        pytest.param(
            "ethereum",
            "mainnet",
            True,
            id="ethereum mainnet",
        ),
        pytest.param(
            "localhost",
            "devnet",
            True,
            id="localhost devnet",
        ),
        pytest.param(
            "solana",
            "mainnet",
            False,
            id="solana mainnet",
        ),
    ],
)
def test_is_supported_network(chain_name, network_name, response):
    network_supported = is_supported_network(
        chain_name=chain_name,
        network_name=network_name,
    )
    assert network_supported is response


@pytest.mark.parametrize(
    ["chain_name", "network_name", "response"],
    [
        pytest.param(
            "ethereum",
            "mainnet",
            "https://ethereum-rpc.publicnode.com",
            id="ethereum mainnet",
        ),
        pytest.param(
            "polygon",
            "amoy",
            "https://rpc-amoy.polygon.technology",
            id="polygon amoy",
        ),
    ],
)
def test_get_default_rpc_endpoint(chain_name, network_name, response):
    rpc_endpoint = get_default_rpc_endpoint(
        chain_name=chain_name,
        network_name=network_name,
    )
    assert rpc_endpoint == response


def test_get_default_rpc_endpoint_failures():
    with pytest.raises(NetworkNotSupported):
        get_default_rpc_endpoint(
            chain_name="ethereum",
            network_name="goerli",
        )
