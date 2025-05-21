from dataclasses import dataclass

import pytest

from packages.core.src.client import SdkClient


@dataclass(frozen=True)
class KnownAccount:
    address: str
    private_key: str


KNOWN_ACCOUNTS = [
    KnownAccount(
        "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
        "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
    ),
    KnownAccount(
        "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
        "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",
    ),
    KnownAccount(
        "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",
        "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a",
    ),
]


@pytest.fixture(scope="function")
def sdk_client():
    return SdkClient(
        chain_name="localhost",
        network_name="devnet",
        private_key=KNOWN_ACCOUNTS[0].private_key,
    )


@pytest.fixture(scope="session")
def sdk_client_without_account():
    return SdkClient(
        chain_name="localhost",
        network_name="devnet",
    )
