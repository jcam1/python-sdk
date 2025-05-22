import sys
import time
from pathlib import Path
from random import randbytes

from eth_account import Account

sys.path.append(str(Path(__file__).parents[1]))

from examples.constants import KNOWN_ACCOUNTS
from examples.main import jpyc_0, jpyc_1
from examples.utils import add_zero_padding_to_hex, remove_decimals


def main() -> None:
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
        "chainId": jpyc_0.client.w3.eth.chain_id,
        "verifyingContract": jpyc_0.contract.address,
    }
    types = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        "ReceiveWithAuthorization": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"},
            {"name": "validAfter", "type": "uint256"},
            {"name": "validBefore", "type": "uint256"},
            {"name": "nonce", "type": "bytes32"},
        ],
    }
    from_ = KNOWN_ACCOUNTS[0].address
    to = KNOWN_ACCOUNTS[1].address
    value = 3000
    valid_after = 0
    valid_before = int(time.time()) + 3600
    nonce = f"0x{randbytes(32).hex()}"

    signed_message = Account.sign_typed_data(
        KNOWN_ACCOUNTS[0].private_key,
        full_message={
            "domain": domain,
            "types": types,
            "primaryType": "ReceiveWithAuthorization",
            "message": {
                "from": from_,
                "to": to,
                "value": remove_decimals(value),  # NOTE: Don't forget decimals handling
                "validAfter": valid_after,
                "validBefore": valid_before,
                "nonce": nonce,
            },
        },
    )

    # 3. Receive JPYC tokens (note that caller here is `KNOWN_ACCOUNTS[1]`)
    jpyc_1.receive_with_authorization(
        from_=from_,
        to=to,
        value=value,
        valid_after=valid_after,
        valid_before=valid_before,
        nonce=nonce,
        v=signed_message.v,
        r=add_zero_padding_to_hex(hex(signed_message.r), 32),
        s=add_zero_padding_to_hex(hex(signed_message.s), 32),
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
