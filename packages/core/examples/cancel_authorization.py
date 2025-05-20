import sys
import time
from pathlib import Path
from random import randbytes

from eth_account import Account

sys.path.append(str(Path(__file__).parents[1]))

from examples.constants import KNOWN_ACCOUNTS
from examples.main import jpyc_0
from examples.utils import add_zero_padding_to_hex, remove_decimals


def main() -> None:
    # 0. Configure a minter
    jpyc_0.configure_minter(
        minter=KNOWN_ACCOUNTS[0].address,
        minter_allowed_amount=1000000,
    )

    # 1. Mint JPYC tokens
    # NOTE: caller here is `KNOWN_ACCOUNTS[0]`
    jpyc_0.mint(
        to=KNOWN_ACCOUNTS[0].address,
        amount=10000,
    )

    # 2. Prepare common typed data
    domain = {
        "name": jpyc_0.contract.functions.name().call(),
        "version": "1",
        "chainId": jpyc_0.client.w3.eth.chain_id,
        "verifyingContract": jpyc_0.contract.address,
    }
    nonce = f"0x{randbytes(32).hex()}"

    # 3. Sign a typed message for`transferWithAuthorization`
    types = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        "TransferWithAuthorization": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"},
            {"name": "validAfter", "type": "uint256"},
            {"name": "validBefore", "type": "uint256"},
            {"name": "nonce", "type": "bytes32"},
        ],
    }
    from_ = KNOWN_ACCOUNTS[0].address
    to = KNOWN_ACCOUNTS[2].address
    value = 3000
    validAfter = 0
    validBefore = int(time.time()) + 3600

    signed_message_transfer = Account.sign_typed_data(
        KNOWN_ACCOUNTS[0].private_key,
        full_message={
            "domain": domain,
            "types": types,
            "primaryType": "TransferWithAuthorization",
            "message": {
                "from": from_,
                "to": to,
                "value": remove_decimals(value),  # NOTE: Don't forget decimals handling
                "validAfter": validAfter,
                "validBefore": validBefore,
                "nonce": nonce,
            },
        },
    )

    # 4. Sign a typed message for `cancelAuthorization`
    types = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        "CancelAuthorization": [
            {"name": "authorizer", "type": "address"},
            {"name": "nonce", "type": "bytes32"},
        ],
    }

    signed_message_cancel = Account.sign_typed_data(
        KNOWN_ACCOUNTS[0].private_key,
        full_message={
            "domain": domain,
            "types": types,
            "primaryType": "CancelAuthorization",
            "message": {
                "authorizer": from_,
                "nonce": nonce,
            },
        },
    )

    # 5. Cancel authorization
    # NOTE: caller here is `KNOWN_ACCOUNTS[0]`
    jpyc_0.cancel_authorization(
        authorizer=from_,
        nonce=nonce,
        v=signed_message_cancel.v,
        r=add_zero_padding_to_hex(hex(signed_message_cancel.r), 32),
        s=add_zero_padding_to_hex(hex(signed_message_cancel.s), 32),
    )

    # 6. Check if authorization has been cancelled
    # NOTE: caller here is `KNOWN_ACCOUNTS[0]`
    try:
        jpyc_0.transfer_with_authorization(
            from_=from_,
            to=to,
            value=value,
            valid_after=validAfter,
            valid_before=validBefore,
            nonce=nonce,
            v=signed_message_transfer.v,
            r=add_zero_padding_to_hex(hex(signed_message_transfer.r), 32),
            s=add_zero_padding_to_hex(hex(signed_message_transfer.s), 32),
        )
    except Exception:
        print("Authorization has been cancelled successfully.")
    else:
        raise Exception("ERROR: authorization has not been cancelled.")


if __name__ == "__main__":
    main()
