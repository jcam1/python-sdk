from dataclasses import dataclass
import time
from random import randbytes

import pytest
from pytest_mock import MockFixture
from web3.contract.contract import (
    ContractConstructor,
    ContractFunction,
)
from web3.eth import Eth

from packages.core.jpyc_core_sdk.client import SdkClient
from packages.core.jpyc_core_sdk.jpyc import JPYC


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


V2_PROXY_ADDRESS = "0x431D5dfF03120AFA4bDf332c61A6e1766eF37BDB"


def add_zero_padding_to_hex(hex_string: str, num_of_bytes: int) -> str:
    return f"0x{hex_string[2:].zfill(num_of_bytes * 2)}"


@pytest.fixture(scope="function")
def sdk_client():
    return SdkClient(
        chain_name="ethereum",
        network_name="mainnet",
        private_key=KNOWN_ACCOUNTS[0].private_key,
    )


@pytest.fixture(scope="function")
def sdk_client_localhost():
    return SdkClient(
        chain_name="localhost",
        network_name="devnet",
        private_key=KNOWN_ACCOUNTS[0].private_key,
    )


@pytest.fixture(scope="session")
def sdk_client_without_account():
    return SdkClient(
        chain_name="ethereum",
        network_name="mainnet",
    )


@pytest.fixture(scope="function")
def jpyc_client(sdk_client, mocker: MockFixture):
    mocker.patch.object(
        Eth,
        "chain_id",
        new_callable=mocker.PropertyMock,
        return_value=1,
    )
    return JPYC(
        client=sdk_client,
        contract_address=V2_PROXY_ADDRESS,
    )


@pytest.fixture(scope="function")
def jpyc_client_without_account(sdk_client_without_account, mocker: MockFixture):
    mocker.patch.object(
        Eth,
        "chain_id",
        new_callable=mocker.PropertyMock,
        return_value=1,
    )
    return JPYC(
        client=sdk_client_without_account,
        contract_address=V2_PROXY_ADDRESS,
    )


@pytest.fixture(scope="function")
def eip712_domain_separator():
    return {
        "name": "JPY Coin",
        "version": "1",
        "chainId": 1,
        "verifyingContract": V2_PROXY_ADDRESS,
    }


@pytest.fixture(scope="function")
def eip712_domain_types():
    return [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "verifyingContract", "type": "address"},
    ]


@pytest.fixture(scope="function")
def valid_before():
    return int(time.time()) + 3600


@pytest.fixture(scope="function")
def nonce():
    return f"0x{randbytes(32).hex()}"


@pytest.fixture(scope="function")
def mocked_eth_chain_id(mocker: MockFixture, request):
    return mocker.patch.object(
        Eth,
        "chain_id",
        new_callable=mocker.PropertyMock,
        return_value=request.param["chain_id"],
    )


@pytest.fixture(scope="function")
def mocked_eth_contract_constructor_transact(mocker: MockFixture):
    return mocker.patch.object(
        ContractConstructor,
        "transact",
        return_value="0x",
    )


@pytest.fixture(scope="function")
def mocked_eth_wait_for_transaction_receipt(mocker: MockFixture, request):
    @dataclass()
    class TxReceipt:
        contractAddress: str

    return mocker.patch.object(
        Eth,
        "wait_for_transaction_receipt",
        return_value=TxReceipt(
            contractAddress=request.param["address"],
        ),
    )


@pytest.fixture(scope="function")
def mocked_eth_contract_functions_transact(mocker: MockFixture):
    return mocker.patch.object(
        ContractFunction,
        "transact",
        return_value="0x",
    )


@pytest.fixture(scope="function")
def mocked_eth_contract_functions(
    mocker: MockFixture,
    jpyc_client,
    request,
):
    if "return_value" in request.param:
        return mocker.patch.object(
            jpyc_client.contract.functions,
            request.param["func_name"],
            return_value=(
                getattr(
                    jpyc_client.contract.functions,
                    request.param["func_name"],
                )(*request.param["func_args"])
                if "func_args" in request.param
                else getattr(
                    jpyc_client.contract.functions,
                    request.param["func_name"],
                )()
            ),
        )
    return mocker.patch.object(
        jpyc_client.contract.functions,
        request.param["func_name"],
    )
