import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from examples.constants import KNOWN_ACCOUNTS
from src.client import SdkClient
from src.jpyc import JPYC

# SDK clients
client_0 = SdkClient(
    chain_name="localhost",
    network_name="devnet",
    private_key=KNOWN_ACCOUNTS[0].private_key,
)
client_1 = SdkClient(
    chain_name="localhost",
    network_name="devnet",
    private_key=KNOWN_ACCOUNTS[1].private_key,
)

# JPYC clients
jpyc_0 = JPYC(
    client=client_0,
)
jpyc_1 = JPYC(
    client=client_1,
    contract_address=jpyc_0.contract.address,
)
