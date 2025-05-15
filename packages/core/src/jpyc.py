from decimal import Decimal

from eth_typing import ChecksumAddress
from web3 import Web3

from core.src.interfaces import IJPYC
from core.src.utils.abis import (
    get_abi,
    resolve_abi_file_path,
)
from core.src.utils.addresses import (
    get_proxy_address,
)
from core.src.utils.constants import sign_middleware
from core.src.utils.currencies import (
    remove_decimals,
    restore_decimals,
)
from core.src.utils.errors import AccountNotInitialized
from core.src.utils.transactions import catch_transaction_errors
from core.src.utils.types import ContractVersion

class JPYC(IJPYC):
    """Implementation of IJPYC."""

    def __init__(
        self,
        w3: Web3,
        contract_version: ContractVersion = "2"
    ):
        """Constructor that initializes JPYC client.

        Args:
            w3 (Web3): Configured web3 instance
            contract_version (ContractVersion): Contract version
        """
        self.w3 = w3
        """Web3: Configured web3 instance"""
        self.contract = w3.eth.contract(
            address=get_proxy_address(contract_version=contract_version),
            abi=get_abi(resolve_abi_file_path(contract_version=contract_version)),
        )
        """Contract: Contract instance"""

    def __account_initialized(self) -> None:
        """Check if account is initialized.

        Note:
            An account must be set to web3 instance to send transactions.

        Raises:
            AccountNotInitialized: If account is not initialized
        """
        if sign_middleware not in self.w3.middleware_onion:
            raise AccountNotInitialized()

    ##################
    # View functions #
    ##################

    def is_minter(self, account: ChecksumAddress) -> bool:
        return self.contact.functions.isMinter(account).call()

    @restore_decimals
    def minter_allowance(self, minter: ChecksumAddress) -> Decimal:
        return self.contact.functions.minterAllowance(minter).call()

    @restore_decimals
    def total_supply(self) -> Decimal:
        return self.contact.functions.totalSupply().call()

    @restore_decimals
    def balance_of(self, account: ChecksumAddress) -> Decimal:
        return self.contact.functions.balanceOf(account).call()

    @restore_decimals
    def allowance(self, owner: ChecksumAddress, spender: ChecksumAddress) -> Decimal:
        return self.contact.functions.allowance(owner, spender).call()

    def nonces(self, owner: ChecksumAddress) -> int:
        return self.contact.functions.nonces(owner).call()

    ######################
    # Mutation functions #
    ######################

    # TODO: transaction simulation using eth.call()

    @catch_transaction_errors
    def configure_minter(self, minter: ChecksumAddress, minter_allowed_amount: Decimal) -> str:
        self.__account_initialized()

        return self.contact.functions.configureMinter(
            minter,
            remove_decimals(minter_allowed_amount),
        ).call()

    @catch_transaction_errors
    def mint(self, to: ChecksumAddress, amount: Decimal) -> str:
        self.__account_initialized()

        return self.contact.functions.mint(
            to,
            remove_decimals(amount),
        ).call()

    @catch_transaction_errors
    def transfer(self, to: ChecksumAddress, value: Decimal) -> str:
        self.__account_initialized()

        return self.contact.functions.transfer(
            to,
            remove_decimals(value),
        ).call()

    @catch_transaction_errors
    def transfer_from(self, from_: ChecksumAddress, to: ChecksumAddress, value: Decimal) -> str:
        self.__account_initialized()

        return self.contact.functions.transferFrom(
            from_,
            to,
            remove_decimals(value),
        ).call()

    @catch_transaction_errors
    def transfer_with_authorization(
        self,
        from_: ChecksumAddress,
        to: ChecksumAddress,
        value: Decimal,
        validAfter: int,
        validBefore: int,
        nonce: str,
        v: int,
        r: str,
        s: str,
    ) -> str:
        self.__account_initialized()

        return self.contact.functions.transferWithAuthorization(
            from_,
            to,
            remove_decimals(value),
            validAfter,
            validBefore,
            nonce,
            v,
            r,
            s,
        ).call()

    @catch_transaction_errors
    def receive_with_authorization(
        self,
        from_: ChecksumAddress,
        to: ChecksumAddress,
        value: Decimal,
        validAfter: int,
        validBefore: int,
        nonce: str,
        v: int,
        r: str,
        s: str,
    ) -> str:
        self.__account_initialized()

        return self.contact.functions.receiveWithAuthorization(
            from_,
            to,
            remove_decimals(value),
            validAfter,
            validBefore,
            nonce,
            v,
            r,
            s,
        ).call()

    @catch_transaction_errors
    def cancel_authorization(
        self,
        authorizer: ChecksumAddress,
        nonce: str,
        v: int,
        r: str,
        s: str,
    ) -> str:
        self.__account_initialized()

        return self.contact.functions.cancelAuthorization(
            authorizer,
            nonce,
            v,
            r,
            s,
        ).call()

    @catch_transaction_errors
    def approve(self, spender: ChecksumAddress, value: Decimal) -> str:
        self.__account_initialized()

        return self.contact.functions.approve(
            spender,
            remove_decimals(value),
        ).call()

    @catch_transaction_errors
    def increase_allowance(self, spender: ChecksumAddress, increment: Decimal) -> str:
        self.__account_initialized()

        return self.contact.functions.increaseAllowance(
            spender,
            remove_decimals(increment),
        ).call()

    @catch_transaction_errors
    def decrease_allowance(self, spender: ChecksumAddress, decrement: Decimal) -> str:
        self.__account_initialized()

        return self.contact.functions.decreaseAllowance(
            spender,
            remove_decimals(decrement),
        ).call()

    @catch_transaction_errors
    def permit(
        self,
        owner: ChecksumAddress,
        spender: ChecksumAddress,
        value: Decimal,
        deadline: int,
        v: int,
        r: str,
        s: str,
    ) -> str:
        self.__account_initialized()

        return self.contact.functions.permit(
            owner,
            spender,
            remove_decimals(value),
            deadline,
            v,
            r,
            s,
        ).call()
