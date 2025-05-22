import pytest

from packages.core.src.utils.errors import (
    InvalidChecksumAddress,
)

from ..conftest import KNOWN_ACCOUNTS


@pytest.mark.parametrize(
    [
        "mocked_eth_contract_functions",
    ],
    [
        pytest.param(
            {
                "func_name": "allowance",
                "func_args": [
                    KNOWN_ACCOUNTS[0].address,
                    KNOWN_ACCOUNTS[1].address,
                ],
                "return_value": 1000000000000000000000,
            },
        ),
    ],
    indirect=[
        "mocked_eth_contract_functions",
    ],
)
def test_allowance(
    jpyc_client,
    mocked_eth_contract_functions,
):
    owner = KNOWN_ACCOUNTS[0].address
    spender = KNOWN_ACCOUNTS[1].address

    jpyc_client.allowance(
        owner=owner,
        spender=spender,
    )

    mocked_eth_contract_functions.assert_called_once_with(owner, spender)


@pytest.mark.parametrize(
    [
        "owner",
        "spender",
    ],
    [
        pytest.param(
            "invalid_address",
            KNOWN_ACCOUNTS[1].address,
            id="invalid owner",
        ),
        pytest.param(
            KNOWN_ACCOUNTS[0].address,
            "invalid_address",
            id="invalid spender",
        ),
    ],
)
def test_allowance_failures(
    jpyc_client,
    owner,
    spender,
):
    with pytest.raises(InvalidChecksumAddress):
        jpyc_client.allowance(
            owner=owner,
            spender=spender,
        )
