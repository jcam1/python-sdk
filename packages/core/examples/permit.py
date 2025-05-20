import sys
import time
from pathlib import Path

from eth_account import Account

sys.path.append(str(Path(__file__).parents[1]))

from examples.constants import KNOWN_ACCOUNTS
from examples.main import jpyc_0
from examples.utils import add_zero_padding_to_hex, remove_decimals


def main():
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
        "Permit": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"},
            {"name": "value", "type": "uint256"},
            {"name": "nonce", "type": "uint256"},
            {"name": "deadline", "type": "uint256"},
        ],
    }
    owner = KNOWN_ACCOUNTS[0].address
    spender = KNOWN_ACCOUNTS[1].address
    value = 3000
    deadline = int(time.time()) + 3600
    nonce = jpyc_0.nonces(owner=owner)

    signed_message = Account.sign_typed_data(
        KNOWN_ACCOUNTS[0].private_key,
        full_message={
            "domain": domain,
            "types": types,
            "primaryType": "Permit",
            "message": {
                "owner": owner,
                "spender": spender,
                "value": remove_decimals(value),  # NOTE: Don't forget decimals handling
                "nonce": nonce,
                "deadline": deadline,
            },
        },
    )

    # 3. Permit `spender` to transfer JPYC tokens on behalf of `owner`
    # NOTE: caller here is `KNOWN_ACCOUNTS[0]`
    jpyc_0.permit(
        owner=owner,
        spender=spender,
        value=value,
        deadline=deadline,
        v=signed_message.v,
        r=add_zero_padding_to_hex(hex(signed_message.r), 32),
        s=add_zero_padding_to_hex(hex(signed_message.s), 32),
    )

    # 4. Check allowance
    allowance = jpyc_0.allowance(
        owner=KNOWN_ACCOUNTS[0].address,
        spender=KNOWN_ACCOUNTS[1].address,
    )
    print(
        f"Allowance of {KNOWN_ACCOUNTS[1].address}"
        f"over {KNOWN_ACCOUNTS[0].address}'s assets: {allowance}"
    )


if __name__ == "__main__":
    main()
