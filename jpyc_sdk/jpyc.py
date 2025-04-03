"""Core module for JPYC token operations"""

import os
from typing import Optional, Union, Dict, Any, Callable, TypeVar, cast
import asyncio
from web3 import Web3
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from hexbytes import HexBytes
from eth_account.signers.local import LocalAccount
from typing_extensions import Self

from .interfaces.jpyc import IJPYC
from .interfaces.abis import JPYC_V2_ABI
from .utils.types import Address, Bytes32, Uint256, Uint8
from .utils.addresses import V2_PROXY_ADDRESS, LOCAL_PROXY_ADDRESS, is_valid_address
from .utils.errors import InvalidAddressError, InvalidTransactionError
from .utils.math import remove_decimals, restore_decimals

T = TypeVar('T')  # Define a type variable

class JPYC(IJPYC):
    """
    Client for interacting with the JPYC token contract.
    """
    
    def __init__(self, web3: Web3, account: Optional[LocalAccount] = None):
        """
        Initialize the JPYC client.
        
        Args:
            web3: Web3 instance
            account: Account to use (optional)
            
        Raises:
            InvalidAddressError: If the contract address is invalid
        """
        self.web3 = web3
        self.account = account
        
        # Determine contract address based on environment
        if os.environ.get('SDK_ENV') == 'local':
            self.contract_address = LOCAL_PROXY_ADDRESS
        else:
            self.contract_address = V2_PROXY_ADDRESS
        
        if not is_valid_address(self.contract_address):
            raise InvalidAddressError(self.contract_address)
        
        # Create contract instance
        self.contract = self.web3.eth.contract(
            address=self.contract_address,
            abi=JPYC_V2_ABI
        )
        
        # Ensure default account is set
        if self.account and not self.web3.eth.default_account:
            self.web3.eth.default_account = self.account.address
    
    # Common async helper methods
    async def _call_async(self, func: Callable[[], T]) -> T:
        """
        Helper method to call synchronous functions asynchronously
        
        Args:
            func: Function to call
            
        Returns:
            The result of the function call
        """
        return await asyncio.to_thread(func)
    
    async def _execute_transaction(self, contract_fn: ContractFunction) -> HexBytes:
        """
        Common helper method for executing transactions
        
        Args:
            contract_fn: Contract function to execute
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction fails
        """
        if not self.account:
            raise InvalidTransactionError(Exception("No account is set"))
        
        if not self.web3.eth.default_account:
            self.web3.eth.default_account = self.account.address
        
        try:
            account = cast(LocalAccount, self.account)
            default_account = cast(Address, self.web3.eth.default_account)

            # Simulation (gas estimation)
            gas_estimate = await self._call_async(
                lambda: contract_fn.estimate_gas({'from': default_account})
            )
            
            # Build transaction
            nonce = await self._call_async(
                lambda: self.web3.eth.get_transaction_count(default_account)
            )
            
            tx = await self._call_async(
                lambda: contract_fn.build_transaction({
                    'from': default_account,
                    'gas': gas_estimate,
                    'nonce': nonce,
                })
            )
            
            # Sign and send transaction
            signed_tx = await self._call_async(
                lambda: self.web3.eth.account.sign_transaction(tx, private_key=account.key)
            )
            
            tx_hash = await self._call_async(
                lambda: self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            )
            
            return tx_hash
            
        except Exception as e:
            # More detailed error handling
            if "insufficient funds" in str(e).lower():
                raise InvalidTransactionError(Exception(f"Insufficient funds: {e}"))
            elif "gas required exceeds allowance" in str(e).lower():
                raise InvalidTransactionError(Exception(f"Gas limit exceeded: {e}"))
            else:
                raise InvalidTransactionError(Exception(f"Transaction error: {e}"))
    
    # View functions (read-only)
    async def is_minter(self, account: Address) -> bool:
        """
        Returns whether the specified address is a minter.
        
        Args:
            account: Account address
            
        Returns:
            bool: True if minter, False otherwise
        """
        return await self._call_async(
            lambda: self.contract.functions.isMinter(account).call()
        )
    
    async def minter_allowance(self, minter: Address) -> float:
        """
        Returns the minter's allowance (for minting).
        
        Args:
            minter: Minter address
            
        Returns:
            int: Minter allowance
        """
        result = await self._call_async(
            lambda: self.contract.functions.minterAllowance(minter).call()
        )
        return restore_decimals(result)
    
    async def total_supply(self) -> float:
        """
        Returns the total supply of JPYC tokens.
        
        Returns:
            int: Total supply
        """
        result = await self._call_async(
            lambda: self.contract.functions.totalSupply().call()
        )
        return restore_decimals(result)
    
    async def balance_of(self, account: Address) -> float:
        """
        Returns the account balance.
        
        Args:
            account: Account address
            
        Returns:
            int: Account balance
        """
        result = await self._call_async(
            lambda: self.contract.functions.balanceOf(account).call()
        )
        return restore_decimals(result)
    
    async def allowance(self, owner: Address, spender: Address) -> float:
        """
        Returns the spender's allowance for the owner's tokens (for transfers).
        
        Args:
            owner: Owner address
            spender: Spender address
            
        Returns:
            int: Spender allowance
        """
        result = await self._call_async(
            lambda: self.contract.functions.allowance(owner, spender).call()
        )
        return restore_decimals(result)
    
    async def nonces(self, owner: Address) -> int:
        """
        Returns the nonce for EIP2612 `permit`.
        
        Args:
            owner: Owner address
            
        Returns:
            int: Owner nonce
        """
        return await self._call_async(
            lambda: self.contract.functions.nonces(owner).call()
        )
    
    # State-changing functions (write)
    async def configure_minter(self, minter: Address, minter_allowed_amount: int) -> HexBytes:
        """
        Configure a minter.
        
        Args:
            minter: Minter address
            minter_allowed_amount: Minter allowance
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        amount_wei = remove_decimals(minter_allowed_amount)
        return await self._execute_transaction(
            self.contract.functions.configureMinter(minter, amount_wei)
        )
    
    async def mint(self, to: Address, amount: Union[int, float]) -> HexBytes:
        """
        Mint tokens.
        
        Args:
            to: Recipient address
            amount: Amount of tokens to mint
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        amount_wei = remove_decimals(amount)
        return await self._execute_transaction(
            self.contract.functions.mint(to, amount_wei)
        )
    
    async def transfer(self, to: Address, value: Union[int, float]) -> HexBytes:
        """
        Transfer tokens (directly).
        
        Args:
            to: Recipient address
            value: Amount of tokens to transfer
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        value_wei = remove_decimals(value)
        return await self._execute_transaction(
            self.contract.functions.transfer(to, value_wei)
        )
    
    async def transfer_from(self, from_address: Address, to: Address, value: Union[int, float]) -> HexBytes:
        """
        Transfer tokens (from spender).
        
        Args:
            from_address: Owner address
            to: Recipient address
            value: Amount of tokens to transfer
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        value_wei = remove_decimals(value)
        return await self._execute_transaction(
            self.contract.functions.transferFrom(from_address, to, value_wei)
        )
    
    async def approve(self, spender: Address, value: Union[int, float]) -> HexBytes:
        """
        Set the spender's allowance for the owner's tokens.
        
        Args:
            spender: Spender address
            value: Allowance
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        value_wei = remove_decimals(value)
        return await self._execute_transaction(
            self.contract.functions.approve(spender, value_wei)
        )
    
    async def increase_allowance(self, spender: Address, increment: Union[int, float]) -> HexBytes:
        """
        Increase allowance.
        
        Args:
            spender: Spender address
            increment: Amount to increase allowance by
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        increment_wei = remove_decimals(increment)
        return await self._execute_transaction(
            self.contract.functions.increaseAllowance(spender, increment_wei)
        )
    
    async def decrease_allowance(self, spender: Address, decrement: Union[int, float]) -> HexBytes:
        """
        Decrease allowance.
        
        Args:
            spender: Spender address
            decrement: Amount to decrease allowance by
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        decrement_wei = remove_decimals(decrement)
        return await self._execute_transaction(
            self.contract.functions.decreaseAllowance(spender, decrement_wei)
        )
    
    async def permit(self, owner: Address, spender: Address, value: Union[int, float], 
                   deadline: Uint256, v: Uint8, r: Bytes32, s: Bytes32) -> HexBytes:
        """
        Set allowance using EIP2612 permit.
        
        Args:
            owner: Owner address
            spender: Spender address
            value: Allowance
            deadline: Deadline
            v: v parameter of the signature
            r: r parameter of the signature
            s: s parameter of the signature
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        value_wei = remove_decimals(value)
        return await self._execute_transaction(
            self.contract.functions.permit(owner, spender, value_wei, deadline, v, r, s)
        )
    
    async def transfer_with_authorization(self, from_address: Address, to: Address, value: Union[int, float],
                                        valid_after: Uint256, valid_before: Uint256, nonce: Bytes32,
                                        v: Uint8, r: Bytes32, s: Bytes32) -> HexBytes:
        """
        Execute a signed transfer.
        
        Args:
            from_address: Sender address
            to: Recipient address
            value: Amount to transfer
            valid_after: Start of validity period
            valid_before: End of validity period
            nonce: Nonce
            v: v parameter of the signature
            r: r parameter of the signature
            s: s parameter of the signature
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        value_wei = remove_decimals(value)
        return await self._execute_transaction(
            self.contract.functions.transferWithAuthorization(
                from_address, to, value_wei, valid_after, valid_before, nonce, v, r, s
            )
        )
    
    async def receive_with_authorization(self, from_address: Address, to: Address, value: Union[int, float],
                                       valid_after: Uint256, valid_before: Uint256, nonce: Bytes32,
                                       v: Uint8, r: Bytes32, s: Bytes32) -> HexBytes:
        """
        Execute a signed receive.
        
        Args:
            from_address: Sender address
            to: Recipient address
            value: Amount to transfer
            valid_after: Start of validity period
            valid_before: End of validity period
            nonce: Nonce
            v: v parameter of the signature
            r: r parameter of the signature
            s: s parameter of the signature
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        value_wei = remove_decimals(value)
        return await self._execute_transaction(
            self.contract.functions.receiveWithAuthorization(
                from_address, to, value_wei, valid_after, valid_before, nonce, v, r, s
            )
        )
    
    async def cancel_authorization(self, authorizer: Address, nonce: Bytes32,
                                 v: Uint8, r: Bytes32, s: Bytes32) -> HexBytes:
        """
        Cancel a signed authorization.
        
        Args:
            authorizer: Authorizer address
            nonce: Nonce
            v: v parameter of the signature
            r: r parameter of the signature
            s: s parameter of the signature
            
        Returns:
            HexBytes: Transaction hash
            
        Raises:
            InvalidTransactionError: If the transaction simulation fails
        """
        return await self._execute_transaction(
            self.contract.functions.cancelAuthorization(authorizer, nonce, v, r, s)
        )