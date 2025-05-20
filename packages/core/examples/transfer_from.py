import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

from examples.constants import KNOWN_ACCOUNTS
from examples.main import jpyc_0, jpyc_1


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

    # 2. Approve `KNOWN_ACCOUNTS[1]` to transfer JPYC tokens
    jpyc_0.approve(
        spender=KNOWN_ACCOUNTS[1].address,
        value=5000,
    )

    # 3. Check allowance
    allowance = jpyc_0.allowance(
        owner=KNOWN_ACCOUNTS[0].address,
        spender=KNOWN_ACCOUNTS[1].address,
    )
    print(
        f"Allowance of {KNOWN_ACCOUNTS[1].address}"
        f"over {KNOWN_ACCOUNTS[0].address}'s assets: {allowance}"
    )

    # 4. Transfer JPYC tokens (note that caller here is `KNOWN_ACCOUNTS[1]`)
    jpyc_1.transfer_from(
        from_=KNOWN_ACCOUNTS[0].address,
        to=KNOWN_ACCOUNTS[2].address,
        value=2500,
    )

    # 5. Check balances
    balance_0 = jpyc_0.balance_of(account=KNOWN_ACCOUNTS[0].address)
    print(f"Balance of {KNOWN_ACCOUNTS[0].address}: {balance_0}")

    balance_1 = jpyc_0.balance_of(account=KNOWN_ACCOUNTS[1].address)
    print(f"Balance of {KNOWN_ACCOUNTS[1].address}: {balance_1}")

    balance_2 = jpyc_0.balance_of(account=KNOWN_ACCOUNTS[2].address)
    print(f"Balance of {KNOWN_ACCOUNTS[2].address}: {balance_2}")


if __name__ == "__main__":
    main()
