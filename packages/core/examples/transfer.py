import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from examples.constants import KNOWN_ACCOUNTS
from examples.main import jpyc_0


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

    # 2. Transfer JPYC tokens (note that caller here is `KNOWN_ACCOUNTS[0]`)
    jpyc_0.transfer(
        to=KNOWN_ACCOUNTS[1].address,
        value=3000,
    )

    # 3. Check balances
    balance_0 = jpyc_0.balance_of(account=KNOWN_ACCOUNTS[0].address)
    print(f"Balance of {KNOWN_ACCOUNTS[0].address}: {balance_0}")

    balance_1 = jpyc_0.balance_of(account=KNOWN_ACCOUNTS[1].address)
    print(f"Balance of {KNOWN_ACCOUNTS[1].address}: {balance_1}")


if __name__ == "__main__":
    main()
