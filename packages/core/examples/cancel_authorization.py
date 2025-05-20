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

    # 2. Prepare common typed data
    domain = {
        "name": jpyc_0.contract.functions.name().call(),
        "version": "1",
        "chainId": 31337,
        "verifyingContract": jpyc_0.contract.address,
    }
    nonce = f"0x{randbytes(32).hex()}"

    # 3. Sign a typed message for`transferWithAuthorization`
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

    # 4. Sign a typed message for `cancelAuthorization`
    types = {
        "EIP712Domain": [
            { "name": "name", "type": "string" },
            { "name": "version", "type": "string" },
            { "name": "chainId", "type": "uint256" },
            { "name": "verifyingContract", "type": "address" },
        ],
        "CancelAuthorization": [
            { "name": "authorizer", "type": "address" },
            { "name": "nonce", "type": "bytes32" },
        ],
    }

    signature = Account.sign_typed_data(
        KNOWN_ACCOUNTS[0].private_key,
        full_message={
            "domain": domain,
            "types": types,
            "primaryType": "CancelAuthorization",
            "message": {
                "authorizer": from_,
                "nonce": nonce,
            },
        }
    )

    # 5. Cancel authorization (note that caller here is `KNOWN_ACCOUNTS[0]`)
    jpyc_0.cancel_authorization(
        authorizer=from_,
        nonce=nonce,
        v=signature.v,
        r=hex(signature.r),
        s=hex(signature.s),
    )

    # 6. Check if authorization has been cancelled (note that caller here is `KNOWN_ACCOUNTS[0]`)
    try:
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
    except Exception as e:
        print(f"Authorization has been successfully cancelled: {e}")

if __name__ == "__main__":
    main()
