from pathlib import Path
from random import randbytes
import sys
import time

from eth_account import Account

sys.path.append(str(Path(__file__).parents[1]))

from examples.constants import KNOWN_ACCOUNTS
from examples.main import jpyc_0
from src.jpyc import *
from src.client import *

# WARNING: this is a broken code example (`EIP3009: invalid signature` is raised)
def main():
    # 0. Configure a minter
    jpyc_0.configure_minter(
        minter=KNOWN_ACCOUNTS[0].address,
        minter_allowed_amount=1000000,
    )

    # 1. Mint JPYC tokens (note that caller here is `KNOWN_ACCOUNTS[0]`)
    jpyc_0.mint(
        to=KNOWN_ACCOUNTS[0].address,
        amount=10000,
    )

    # 2. Sign a typed message
    domain = {
        "name": jpyc_0.contract.functions.name().call(),
        "version": "1",
        "chainId": 31337,
        "verifyingContract": jpyc_0.contract.address,
    }
    types = {
        "EIP712Domain": [
            { "name": "name", "type": "string" },
            { "name": "version", "type": "string" },
            { "name": "chainId", "type": "uint256" },
            { "name": "verifyingContract", "type": "address" },
        ],
        "TransferWithAuthorization": [
            { "name": "from", "type": "address" },
            { "name": "to", "type": "address" },
            { "name": "value", "type": "uint256" },
            { "name": "validAfter", "type": "uint256" },
            { "name": "validBefore", "type": "uint256" },
            { "name": "nonce", "type": "bytes32" },
        ],
    }
    from_ = KNOWN_ACCOUNTS[0].address
    to = KNOWN_ACCOUNTS[2].address
    value = 3000
    validAfter = 0
    validBefore = int(time.time()) + 3600
    nonce = f"0x{randbytes(32).hex()}"

    signature = Account.sign_typed_data(
        KNOWN_ACCOUNTS[0].private_key,
        full_message={
            "domain": domain,
            "types": types,
            "primaryType": "TransferWithAuthorization",
            "message": {
                "from": from_,
                "to": to,
                "value": value,
                "validAfter": validAfter,
                "validBefore": validBefore,
                "nonce": nonce,
            },
        }
    )

    # 3. Transfer JPYC tokens (note that caller here is `KNOWN_ACCOUNTS[0]`)
    jpyc_0.transfer_with_authorization(
        from_=from_,
        to=to,
        value=value,
        valid_after=validAfter,
        valid_before=validBefore,
        nonce=nonce,
        v=signature.v,
        r=hex(signature.r),
        s=hex(signature.s),
    )

    # 4. Check balances
    balance_0 = jpyc_0.balance_of(account=KNOWN_ACCOUNTS[0].address)
    print(f"Balance of {KNOWN_ACCOUNTS[0].address}: {balance_0}")

    balance_1 = jpyc_0.balance_of(account=KNOWN_ACCOUNTS[1].address)
    print(f"Balance of {KNOWN_ACCOUNTS[1].address}: {balance_1}")

    balance_2 = jpyc_0.balance_of(account=KNOWN_ACCOUNTS[2].address)
    print(f"Balance of {KNOWN_ACCOUNTS[2].address}: {balance_2}")

if __name__ == "__main__":
    main()
