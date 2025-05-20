import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from examples.constants import KNOWN_ACCOUNTS
from examples.main import jpyc_0


def main():
    # 0. Check initial total supply of jpyc tokens
    total_supply = jpyc_0.total_supply()
    print(f"Total Supply (before minting): {total_supply}")

    # 1. Configure a minter
    jpyc_0.configure_minter(
        minter=KNOWN_ACCOUNTS[0].address,
        minter_allowed_amount=1000000,
    )

    # 2. Check minter validity
    is_minter_0 = jpyc_0.is_minter(account=KNOWN_ACCOUNTS[0].address)
    print(f"Is {KNOWN_ACCOUNTS[0].address} a minter?: {is_minter_0}")

    is_minter_1 = jpyc_0.is_minter(account=KNOWN_ACCOUNTS[1].address)
    print(f"Is {KNOWN_ACCOUNTS[1].address} a minter?: {is_minter_1}")

    # 3. Check minter allowance
    minter_allowance = jpyc_0.minter_allowance(minter=KNOWN_ACCOUNTS[0].address)
    print(f"Minter allowance of {KNOWN_ACCOUNTS[0].address}: {minter_allowance}")

    # 4. Mint jpyc tokens (note that caller here is `KNOWN_ACCOUNTS[0]`)
    jpyc_0.mint(
        to=KNOWN_ACCOUNTS[1].address,
        amount=10000,
    )

    # 5. Check balance of receiver address
    balance = jpyc_0.balance_of(account=KNOWN_ACCOUNTS[1].address)
    print(f"Balance of {KNOWN_ACCOUNTS[1].address}: {balance}")

    # 6. Check total supply of jpyc tokens after minting
    total_supply = jpyc_0.total_supply()
    print(f"Total Supply (after minting): {total_supply}")


if __name__ == "__main__":
    main()
