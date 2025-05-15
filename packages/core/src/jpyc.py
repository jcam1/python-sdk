from decimal import Decimal
from typing import Any

from eth_typing import ChecksumAddress
from web3.contract.contract import ContractFunction

from interfaces import IJPYC, ISdkClient
from utils.abis import (
    get_abi,
    resolve_abi_file_path,
)
from utils.addresses import (
    get_proxy_address,
)
from utils.constants import sign_middleware
from utils.currencies import (
    remove_decimals,
    restore_decimals,
)
from utils.errors import AccountNotInitialized, TransactionSimulationFailed
from utils.transactions import catch_transaction_errors
from utils.types import ContractVersion

class JPYC(IJPYC):
    """Implementation of IJPYC."""

    def __init__(
        self,
        client: ISdkClient,
        contract_version: ContractVersion = "2"
    ):
        """Constructor that initializes JPYC client.

        Args:
            client (ISdkClient): Configured SDK client
            contract_version (ContractVersion): Contract version
        """
        self.client = client
        """ISdkClient: Configured SDK client"""
        self.contract = client.w3.eth.contract(
            address=get_proxy_address(contract_version=contract_version),
            abi=get_abi(resolve_abi_file_path(contract_version=contract_version)),
        )
        """Contract: Configured contract instance"""

    def __account_initialized(self) -> None:
        """Check if account is initialized.

        Note:
            An account must be set to web3 instance to send transactions.

        Raises:
            AccountNotInitialized: If account is not initialized
        """
        if sign_middleware not in self.client.w3.middleware_onion:
            raise AccountNotInitialized()

    def __simulate_transaction(self, contract_func: ContractFunction, func_args: dict[Any]) -> None:
        """Simulate a transaction locally.

        Note:
            This method should be called before sending actual transactions.

        Raises:
            TransactionSimulationFailed: If transaction simulation fails
        """
        try:
            contract_func.call(**func_args)
        except Exception as e:
            raise TransactionSimulationFailed(e)

    ##################
    # View functions #
    ##################

    def is_minter(self, account: ChecksumAddress) -> bool:
        return self.contract.functions.isMinter(account).call()

    @restore_decimals
    def minter_allowance(self, minter: ChecksumAddress) -> Decimal:
        return self.contract.functions.minterAllowance(minter).call()

    @restore_decimals
    def total_supply(self) -> Decimal:
        return self.contract.functions.totalSupply().call()

    @restore_decimals
    def balance_of(self, account: ChecksumAddress) -> Decimal:
        return self.contract.functions.balanceOf(account).call()

    @restore_decimals
    def allowance(self, owner: ChecksumAddress, spender: ChecksumAddress) -> Decimal:
        return self.contract.functions.allowance(owner, spender).call()

    def nonces(self, owner: ChecksumAddress) -> int:
        return self.contract.functions.nonces(owner).call()

    ######################
    # Mutation functions #
    ######################

    @catch_transaction_errors
    def configure_minter(self, minter: ChecksumAddress, minter_allowed_amount: Decimal) -> str:
        self.__account_initialized()

        args = {
            "minter": minter,
            "minterAllowedAmount": remove_decimals(minter_allowed_amount),
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.configureMinter,
            func_args=args
        )

        return self.contract.functions.configureMinter(**args).transact()

    @catch_transaction_errors
    def mint(self, to: ChecksumAddress, amount: Decimal) -> str:
        self.__account_initialized()

        args = {
            "to": to,
            "amount": remove_decimals(amount),
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.mint,
            func_args=args
        )

        return self.contract.functions.mint(**args).transact()

    @catch_transaction_errors
    def transfer(self, to: ChecksumAddress, value: Decimal) -> str:
        self.__account_initialized()

        args = {
            "to": to,
            "value": remove_decimals(value),
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.transfer,
            func_args=args
        )

        return self.contract.functions.transfer(**args).transact()

    @catch_transaction_errors
    def transfer_from(self, from_: ChecksumAddress, to: ChecksumAddress, value: Decimal) -> str:
        self.__account_initialized()

        args = {
            "from": from_,
            "to": to,
            "value": remove_decimals(value),
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.transferFrom,
            func_args=args
        )

        return self.contract.functions.transferFrom(**args).transact()

    @catch_transaction_errors
    def transfer_with_authorization(
        self,
        from_: ChecksumAddress,
        to: ChecksumAddress,
        value: Decimal,
        valid_after: int,
        valid_before: int,
        nonce: str,
        v: int,
        r: str,
        s: str,
    ) -> str:
        self.__account_initialized()

        args = {
            "from": from_,
            "to": to,
            "value": remove_decimals(value),
            "validAfter": valid_after,
            "validBefore": valid_before,
            "nonce": nonce,
            "v": v,
            "r": r,
            "s": s,
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.transferWithAuthorization,
            func_args=args
        )

        return self.contract.functions.transferWithAuthorization(**args).transact()

    @catch_transaction_errors
    def receive_with_authorization(
        self,
        from_: ChecksumAddress,
        to: ChecksumAddress,
        value: Decimal,
        valid_after: int,
        valid_before: int,
        nonce: str,
        v: int,
        r: str,
        s: str,
    ) -> str:
        self.__account_initialized()

        args = {
            "from": from_,
            "to": to,
            "value": remove_decimals(value),
            "validAfter": valid_after,
            "validBefore": valid_before,
            "nonce": nonce,
            "v": v,
            "r": r,
            "s": s,
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.receiveWithAuthorization,
            func_args=args
        )

        return self.contract.functions.receiveWithAuthorization(**args).transact()

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

        args = {
            "authorizer": authorizer,
            "nonce": nonce,
            "v": v,
            "r": r,
            "s": s,
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.cancelAuthorization,
            func_args=args
        )

        return self.contract.functions.cancelAuthorization(**args).transact()

    @catch_transaction_errors
    def approve(self, spender: ChecksumAddress, value: Decimal) -> str:
        self.__account_initialized()

        args = {
            "spender": spender,
            "value": remove_decimals(value),
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.approve,
            func_args=args
        )

        return self.contract.functions.approve(**args).transact()

    @catch_transaction_errors
    def increase_allowance(self, spender: ChecksumAddress, increment: Decimal) -> str:
        self.__account_initialized()

        args = {
            "spender": spender,
            "increment": remove_decimals(increment),
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.increaseAllowance,
            func_args=args
        )

        return self.contract.functions.increaseAllowance(**args).transact()

    @catch_transaction_errors
    def decrease_allowance(self, spender: ChecksumAddress, decrement: Decimal) -> str:
        self.__account_initialized()

        args = {
            "spender": spender,
            "decrement": remove_decimals(decrement),
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.decreaseAllowance,
            func_args=args
        )

        return self.contract.functions.decreaseAllowance(**args).transact()

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

        args = {
            "owner": owner,
            "spender": spender,
            "value": remove_decimals(value),
            "deadline": deadline,
            "v": v,
            "r": r,
            "s": s,
        }

        self.__simulate_transaction(
            contract_func=self.contract.functions.permit,
            func_args=args
        )

        return self.contract.functions.permit(**args).transact()
