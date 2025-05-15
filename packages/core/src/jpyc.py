from typing import Any

from pydantic import validate_call
from web3.contract.contract import ContractFunction

from interfaces import IJPYC, ISdkClient
from utils.abis import (
    get_abi,
    resolve_abi_file_path,
)
from utils.addresses import (
    get_proxy_address,
)
from utils.constants import SIGN_MIDDLEWARE
from utils.currencies import (
    remove_decimals,
    restore_decimals,
)
from utils.errors import (
    AccountNotInitialized,
    TransactionFailedToSend,
    TransactionSimulationFailed,
)
from utils.types import ContractVersion
from utils.validators import Bytes32, ChecksumAddress, Uint256, Uint8

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

    ##################
    # Helper methods #
    ##################

    def __account_initialized(self) -> None:
        """Checks if account is initialized.

        Note:
            An account must be set to web3 instance to send transactions.

        Raises:
            AccountNotInitialized: If account is not initialized
        """
        if SIGN_MIDDLEWARE not in self.client.w3.middleware_onion:
            raise AccountNotInitialized()

    def __simulate_transaction(self, contract_func: ContractFunction, func_args: dict[Any]) -> None:
        """Simulates a transaction locally.

        Note:
            This method should be called before sending actual transactions.

        Args:
            contract_func (ContractFunction): Contract function
            func_args (dict[Any]): Arguments of contract function

        Raises:
            TransactionSimulationFailed: If transaction simulation fails
        """
        try:
            contract_func.call(**func_args)
        except Exception as e:
            raise TransactionSimulationFailed(e)

    def __send_transaction(self, contract_func: ContractFunction, func_args: dict[Any]) -> Any:
        """Sends a transaction to blockchain.

        Args:
            contract_func (ContractFunction): Contract function
            func_args (dict[Any]): Arguments of contract function

        Returns:
            Any: Response from the contract function

        Raises:
            TransactionFailedToSend: If it fails to send a transaction
        """
        try:
            return contract_func(**func_args).transact()
        except Exception as e:
            raise TransactionFailedToSend(e)

    def __transact(self, contract_func: ContractFunction, func_args: dict[Any]) -> Any:
        """Helper method to prepare & send a transaction in one method.

        Args:
            tx_args (TransactionArgs): Arguments necessary to send a transaction

        Returns:
            Any: Response from the contract function

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionSimulationFailed: If transaction simulation fails
            TransactionFailedToSend: If it fails to send a transaction
        """

        self.__account_initialized()
        self.__simulate_transaction(
            contract_func,
            func_args,
        )
        return self.__send_transaction(
            contract_func,
            func_args,
        )

    ##################
    # View functions #
    ##################

    @validate_call
    def is_minter(self, account: ChecksumAddress) -> bool:
        return self.contract.functions.isMinter(account).call()

    @restore_decimals
    @validate_call
    def minter_allowance(self, minter: ChecksumAddress) -> Uint256:
        return self.contract.functions.minterAllowance(minter).call()

    @restore_decimals
    def total_supply(self) -> Uint256:
        return self.contract.functions.totalSupply().call()

    @restore_decimals
    @validate_call
    def balance_of(self, account: ChecksumAddress) -> Uint256:
        return self.contract.functions.balanceOf(account).call()

    @restore_decimals
    @validate_call
    def allowance(self, owner: ChecksumAddress, spender: ChecksumAddress) -> Uint256:
        return self.contract.functions.allowance(owner, spender).call()

    @validate_call
    def nonces(self, owner: ChecksumAddress) -> Uint256:
        return self.contract.functions.nonces(owner).call()

    ######################
    # Mutation functions #
    ######################

    @validate_call
    def configure_minter(self, minter: ChecksumAddress, minter_allowed_amount: Uint256) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.configureMinter,
            "func_args": {
                "minter": minter,
                "minterAllowedAmount": remove_decimals(minter_allowed_amount),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def mint(self, to: ChecksumAddress, amount: Uint256) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.mint,
            "func_args": {
                "to": to,
                "amount": remove_decimals(amount),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def transfer(self, to: ChecksumAddress, value: Uint256) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.transfer,
            "func_args": {
                "to": to,
                "value": remove_decimals(value),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def transfer_from(self, from_: ChecksumAddress, to: ChecksumAddress, value: Uint256) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.transferFrom,
            "func_args": {
                "from": from_,
                "to": to,
                "value": remove_decimals(value),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def transfer_with_authorization(
        self,
        from_: ChecksumAddress,
        to: ChecksumAddress,
        value: Uint256,
        valid_after: Uint256,
        valid_before: Uint256,
        nonce: Bytes32,
        v: Uint8,
        r: Bytes32,
        s: Bytes32,
    ) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.transferWithAuthorization,
            "func_args": {
                "from": from_,
                "to": to,
                "value": remove_decimals(value),
                "validAfter": valid_after,
                "validBefore": valid_before,
                "nonce": nonce,
                "v": v,
                "r": r,
                "s": s,
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def receive_with_authorization(
        self,
        from_: ChecksumAddress,
        to: ChecksumAddress,
        value: Uint256,
        valid_after: Uint256,
        valid_before: Uint256,
        nonce: Bytes32,
        v: Uint8,
        r: Bytes32,
        s: Bytes32,
    ) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.receiveWithAuthorization,
            "func_args": {
                "from": from_,
                "to": to,
                "value": remove_decimals(value),
                "validAfter": valid_after,
                "validBefore": valid_before,
                "nonce": nonce,
                "v": v,
                "r": r,
                "s": s,
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def cancel_authorization(
        self,
        authorizer: ChecksumAddress,
        nonce: Bytes32,
        v: Uint8,
        r: Bytes32,
        s: Bytes32,
    ) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.cancelAuthorization,
            "func_args": {
                "authorizer": authorizer,
                "nonce": nonce,
                "v": v,
                "r": r,
                "s": s,
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def approve(self, spender: ChecksumAddress, value: Uint256) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.approve,
            "func_args": {
                "spender": spender,
                "value": remove_decimals(value),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def increase_allowance(self, spender: ChecksumAddress, increment: Uint256) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.increaseAllowance,
            "func_args": {
                "spender": spender,
                "increment": remove_decimals(increment),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def decrease_allowance(self, spender: ChecksumAddress, decrement: Uint256) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.decreaseAllowance,
            "func_args": {
                "spender": spender,
                "decrement": remove_decimals(decrement),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def permit(
        self,
        owner: ChecksumAddress,
        spender: ChecksumAddress,
        value: Uint256,
        deadline: Uint256,
        v: Uint8,
        r: Bytes32,
        s: Bytes32,
    ) -> Bytes32:
        tx_args = {
            "contract_func": self.contract.functions.permit,
            "func_args": {
                "owner": owner,
                "spender": spender,
                "value": remove_decimals(value),
                "deadline": deadline,
                "v": v,
                "r": r,
                "s": s,
            },
        }

        return self.__transact(**tx_args)
