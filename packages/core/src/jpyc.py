from typing import Any

from eth_typing import ChecksumAddress as EthChecksumAddress
from pydantic import validate_call
from web3.contract.contract import Contract, ContractFunction

from .client import SdkClient
from .interfaces import IJPYC
from .utils.addresses import (
    get_proxy_address,
)
from .utils.artifacts import (
    get_artifacts,
    resolve_artifacts_file_path,
)
from .utils.chains import SUPPORTED_CHAINS
from .utils.constants import SIGN_MIDDLEWARE
from .utils.currencies import (
    remove_decimals,
    restore_decimals,
)
from .utils.errors import (
    AccountNotInitialized,
    TransactionFailed,
    TransactionSimulationFailed,
)
from .utils.types import ContractVersion, TransactionArgs
from .utils.validators import Bytes32, ChecksumAddress, Uint8, Uint256


class JPYC(IJPYC):
    """Implementation of IJPYC."""

    def __init__(
        self,
        client: SdkClient,
        contract_version: ContractVersion = "2",
        contract_address: EthChecksumAddress | None = None,
    ) -> None:
        """Constructor that initializes JPYC client.

        Notes:
            - If `client` parameter is configured to use localhost network,\
            this deploys JPYC contracts to localhost network, initializes it,\
            and sets its address to `address` attribute.
            - If `contract_address` is supplied,\
            this configures contract instance with that address.

        Args:
            client (SdkClient): Configured SDK client
            contract_version (ContractVersion): Contract version
            contract_address (EthChecksumAddress, optional): Contract address
        """
        if (
            client.w3.eth.chain_id == SUPPORTED_CHAINS["localhost"]["devnet"]["id"]
            and contract_address is None
        ):
            address = self.__deploy_contract(
                client=client,
                contract_version=contract_version,
            )
            contract = self.__get_contract(
                client=client,
                contract_address=address,
                contract_version=contract_version,
            )
            self.__initialize_contract(
                client=client,
                contract=contract,
            )
        else:
            address = (
                contract_address
                if contract_address is not None
                else get_proxy_address(contract_version=contract_version)
            )
            contract = self.__get_contract(
                client=client,
                contract_address=address,
                contract_version=contract_version,
            )

        self.client = client
        """ISdkClient: Configured SDK client"""
        self.contract = contract
        """Contract: Configured contract instance"""

    ##################
    # Helper methods #
    ##################

    @staticmethod
    def __deploy_contract(
        client: SdkClient,
        contract_version: ContractVersion = "2",
    ) -> ChecksumAddress:
        """Deploy contracts to the configured network.

        Note:
            This helper method is mainly for development purposes. \
            Please use this method to deploy contracts to localhost network.

        Args:
            client (SdkClient): Configured SDK client
            contract_version (ContractVersion): Contract version

        Returns:
            ChecksumAddress: Address of the deployed contracts
        """
        file_path = resolve_artifacts_file_path(contract_version=contract_version)
        contract = client.w3.eth.contract(
            abi=get_artifacts(file_path, "abi"),
            bytecode=get_artifacts(file_path, "bytecode"),
        )
        tx_hash = contract.constructor().transact()

        return client.w3.eth.wait_for_transaction_receipt(tx_hash).contractAddress  # type: ignore[attr-defined]

    @staticmethod
    def __get_contract(
        client: SdkClient,
        contract_address: ChecksumAddress,
        contract_version: ContractVersion = "2",
    ) -> Contract:
        """Get contract instance from the configured network.

        Args:
            client (SdkClient): Configured SDK client
            contract_address (ChecksumAddress): Contract address
            contract_version (ContractVersion): Contract version

        Returns:
            Contract: Address of the deployed contracts
        """
        return client.w3.eth.contract(  # type: ignore[call-overload]
            address=contract_address,
            abi=get_artifacts(
                file_path=resolve_artifacts_file_path(
                    contract_version=contract_version
                ),
                artifact_type="abi",
            ),
        )

    @staticmethod
    def __initialize_contract(
        client: SdkClient,
        contract: Contract,
    ) -> None:
        """Initialize contract.

        Args:
            client (SdkClient): Configured SDK client
            contract (Contract): Configured contract instance
        """
        owner_address = client.get_account_address()
        contract.functions.initialize(
            "JPY Coin",
            "JPYC",
            "Yen",
            18,
            owner_address,
            owner_address,
            owner_address,
            owner_address,
            owner_address,
        ).transact()

    def __account_initialized(self) -> None:
        """Checks if account is initialized.

        Note:
            An account must be set to web3 instance to send transactions.

        Raises:
            AccountNotInitialized: If account is not initialized
        """
        if SIGN_MIDDLEWARE not in self.client.w3.middleware_onion:
            raise AccountNotInitialized()

    @staticmethod
    def __simulate_transaction(
        contract_func: ContractFunction,
        func_args: dict[str, object],
    ) -> None:
        """Simulates a transaction locally.

        Note:
            This method should be called before sending actual transactions.

        Args:
            contract_func (ContractFunction): Contract function
            func_args (dict[str, object]): Arguments of contract function

        Raises:
            TransactionSimulationFailed: If transaction simulation fails
        """
        try:
            contract_func(**func_args).call()
        except Exception as e:
            raise TransactionSimulationFailed(str(e))

    @staticmethod
    def __send_transaction(
        contract_func: ContractFunction,
        func_args: dict[str, object],
    ) -> Any:
        """Sends a transaction to blockchain.

        Args:
            contract_func (ContractFunction): Contract function
            func_args (dict[str, object]): Arguments of contract function

        Returns:
            Any: Response from the contract function

        Raises:
            TransactionFailed: If transaction fails
        """
        try:
            return contract_func(**func_args).transact()
        except Exception as e:
            raise TransactionFailed(str(e))

    def __transact(
        self, contract_func: ContractFunction, func_args: dict[str, object]
    ) -> Any:
        """Helper method to prepare & send a transaction in one method.

        Args:
            contract_func (ContractFunction): Contract function
            func_args (dict[str, object]): Arguments of contract function

        Returns:
            Any: Response from the contract function

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionSimulationFailed: If transaction simulation fails
            TransactionFailed: If transaction fails
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
    def configure_minter(
        self, minter: ChecksumAddress, minter_allowed_amount: Uint256
    ) -> Bytes32:
        tx_args: TransactionArgs = {
            "contract_func": self.contract.functions.configureMinter,
            "func_args": {
                "minter": minter,
                "minterAllowedAmount": remove_decimals(minter_allowed_amount),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def mint(self, to: ChecksumAddress, amount: Uint256) -> Bytes32:
        tx_args: TransactionArgs = {
            "contract_func": self.contract.functions.mint,
            "func_args": {
                "_to": to,
                "_amount": remove_decimals(amount),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def transfer(self, to: ChecksumAddress, value: Uint256) -> Bytes32:
        tx_args: TransactionArgs = {
            "contract_func": self.contract.functions.transfer,
            "func_args": {
                "to": to,
                "value": remove_decimals(value),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def transfer_from(
        self, from_: ChecksumAddress, to: ChecksumAddress, value: Uint256
    ) -> Bytes32:
        tx_args: TransactionArgs = {
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
        tx_args: TransactionArgs = {
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
        tx_args: TransactionArgs = {
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
        tx_args: TransactionArgs = {
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
        tx_args: TransactionArgs = {
            "contract_func": self.contract.functions.approve,
            "func_args": {
                "spender": spender,
                "value": remove_decimals(value),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def increase_allowance(
        self, spender: ChecksumAddress, increment: Uint256
    ) -> Bytes32:
        tx_args: TransactionArgs = {
            "contract_func": self.contract.functions.increaseAllowance,
            "func_args": {
                "spender": spender,
                "increment": remove_decimals(increment),
            },
        }

        return self.__transact(**tx_args)

    @validate_call
    def decrease_allowance(
        self, spender: ChecksumAddress, decrement: Uint256
    ) -> Bytes32:
        tx_args: TransactionArgs = {
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
        tx_args: TransactionArgs = {
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
