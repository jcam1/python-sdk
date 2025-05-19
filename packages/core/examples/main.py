from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from src.jpyc import *
from src.client import *

from examples.constants import KNOWN_ACCOUNTS

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
