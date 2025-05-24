import pytest


@pytest.mark.parametrize(
    [
        "mocked_eth_contract_functions",
    ],
    [
        pytest.param(
            {
                "func_name": "totalSupply",
                "return_value": 100000000000000000000000000,
            },
        ),
    ],
    indirect=[
        "mocked_eth_contract_functions",
    ],
)
def test_total_supply(
    jpyc_client,
    mocked_eth_contract_functions,
):
    jpyc_client.total_supply()

    mocked_eth_contract_functions.assert_called_once()
