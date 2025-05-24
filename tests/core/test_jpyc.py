import pytest
from web3.contract.contract import Contract

from packages.core.jpyc_core_sdk.jpyc import JPYC

from .conftest import V2_PROXY_ADDRESS


@pytest.mark.parametrize(
    [
        "contract_address",
        "mocked_eth_chain_id",
    ],
    [
        pytest.param(
            None,
            {"chain_id": 1},
            id="default contract address",
        ),
        pytest.param(
            "0xC8CD2BE653759aed7B0996315821AAe71e1FEAdF",
            {"chain_id": 1},
            id="custom contract address",
        ),
    ],
    indirect=[
        "mocked_eth_chain_id",
    ],
)
def test_constructor(
    sdk_client,
    contract_address,
    mocked_eth_chain_id,
):
    address = V2_PROXY_ADDRESS if contract_address is None else contract_address

    jpyc = JPYC(
        client=sdk_client,
        contract_address=address,
    )

    mocked_eth_chain_id.assert_called_once()

    assert jpyc.client == sdk_client
    assert isinstance(jpyc.contract, Contract)
    assert jpyc.contract.address == address


@pytest.mark.parametrize(
    [
        "mocked_eth_chain_id",
    ],
    [
        pytest.param(
            {"chain_id": 31337},
            id="default contract address",
        ),
    ],
    indirect=[
        "mocked_eth_chain_id",
    ],
)
def test_constructor_localhost(
    sdk_client_localhost,
    mocked_eth_chain_id,
):
    address = "0xC8CD2BE653759aed7B0996315821AAe71e1FEAdF"

    jpyc = JPYC(
        client=sdk_client_localhost,
        contract_address=address,
    )

    mocked_eth_chain_id.assert_called_once()

    assert jpyc.client == sdk_client_localhost
    assert isinstance(jpyc.contract, Contract)
    assert jpyc.contract.address == address


@pytest.mark.parametrize(
    [
        "mocked_eth_chain_id",
        "mocked_eth_wait_for_transaction_receipt",
    ],
    [
        pytest.param(
            {"chain_id": 31337},
            {"address": V2_PROXY_ADDRESS},
            id="default contract address",
        ),
    ],
    indirect=[
        "mocked_eth_chain_id",
        "mocked_eth_wait_for_transaction_receipt",
    ],
)
def test_constructor_localhost_with_deployment(
    sdk_client_localhost,
    mocked_eth_chain_id,
    mocked_eth_contract_constructor_transact,
    mocked_eth_wait_for_transaction_receipt,
    mocked_eth_contract_functions_transact,
):
    jpyc = JPYC(
        client=sdk_client_localhost,
    )

    mocked_eth_chain_id.assert_called_once()
    mocked_eth_contract_constructor_transact.assert_called_once()
    mocked_eth_wait_for_transaction_receipt.assert_called_once()
    mocked_eth_contract_functions_transact.assert_called_once()

    assert jpyc.client == sdk_client_localhost
    assert isinstance(jpyc.contract, Contract)
    assert jpyc.contract.address == V2_PROXY_ADDRESS
