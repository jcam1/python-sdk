"""
Interface definitions for JPYC token operations
"""

from typing import Protocol, Union
from hexbytes import HexBytes

from ..utils.types import Address, Bytes32, Uint256, Uint8

class IJPYC(Protocol):
    """
    Interface for JPYC token operations
    
    This interface defines the methods required to interact with 
    the JPYC stablecoin.
    """
    
    # View関数
    
    async def is_minter(self, account: Address) -> bool:
        """
        Check if an address is a minter
        
        Args:
            account: Address to check
            
        Returns:
            bool: True if the address is a minter, False otherwise
        """
        ...
    
    async def minter_allowance(self, minter: Address) -> float:
        """
        Get the minting allowance for a minter
        
        Args:
            minter: Minter address
            
        Returns:
            int: Minting allowance amount
        """
        ...
    
    async def total_supply(self) -> float:
        """
        Get the total token supply
        
        Returns:
            int: Total supply amount
        """
        ...
    
    async def balance_of(self, account: Address) -> float:
        """
        Get the token balance of an account
        
        Args:
            account: Account address
            
        Returns:
            int: Account balance
        """
        ...
    
    async def allowance(self, owner: Address, spender: Address) -> float:
        """
        Get the spending allowance for a spender
        
        Args:
            owner: Token owner address
            spender: Spender address
            
        Returns:
            int: Allowance amount
        """
        ...
    
    async def nonces(self, owner: Address) -> int:
        """
        Get the current nonce for an address (used for EIP-2612 permits)
        
        Args:
            owner: Owner address
            
        Returns:
            int: Current nonce
        """
        ...
    
    # トランザクション関数
    
    async def configure_minter(self, minter: Address, minter_allowed_amount: int) -> HexBytes:
        """
        ミンターを構成します。
        
        Args:
            minter: ミンターアドレス
            minter_allowed_amount: ミンター許容量
            
        Returns:
            HexBytes: トランザクションハッシュ
        """
        ...
    
    async def mint(self, to: Address, amount: Union[int, float]) -> HexBytes:
        """
        トークンをミントします。
        
        Args:
            to: 受信者アドレス
            amount: ミントするトークンの量
            
        Returns:
            HexBytes: トランザクションハッシュ
        """
        ...
    
    async def transfer(self, to: Address, value: Union[int, float]) -> HexBytes:
        """
        Transfer tokens to another address
        
        Args:
            to: Recipient address
            value: Amount to transfer
            
        Returns:
            HexBytes: Transaction hash
        """
        ...
    
    async def transfer_from(self, from_address: Address, to: Address, value: Union[int, float]) -> HexBytes:
        """
        Transfer tokens from one address to another (requires approval)
        
        Args:
            from_address: Sender address
            to: Recipient address
            value: Amount to transfer
            
        Returns:
            HexBytes: Transaction hash
        """
        ...
    
    async def approve(self, spender: Address, value: Union[int, float]) -> HexBytes:
        """
        Approve a spender to transfer tokens
        
        Args:
            spender: Spender address
            value: Amount to approve
            
        Returns:
            HexBytes: Transaction hash
        """
        ...
    
    async def increase_allowance(self, spender: Address, increment: Union[int, float]) -> HexBytes:
        """
        Increase the spending allowance for a spender
        
        Args:
            spender: Spender address
            increment: Amount to increase the allowance by
            
        Returns:
            HexBytes: Transaction hash
        """
        ...
    
    async def decrease_allowance(self, spender: Address, decrement: Union[int, float]) -> HexBytes:
        """
        Decrease the spending allowance for a spender
        
        Args:
            spender: Spender address
            decrement: Amount to decrease the allowance by
            
        Returns:
            HexBytes: Transaction hash
        """
        ...
    
    async def permit(self, owner: Address, spender: Address, value: Union[int, float], 
                     deadline: Uint256, v: Uint8, r: Bytes32, s: Bytes32) -> HexBytes:
        """
        Set allowance using EIP-2612 permit (gasless approval)
        
        Args:
            owner: Token owner address
            spender: Spender address
            value: Amount to approve
            deadline: Permit expiration timestamp
            v: Signature v parameter
            r: Signature r parameter
            s: Signature s parameter
            
        Returns:
            HexBytes: Transaction hash
        """
        ...
    
    async def transfer_with_authorization(self, from_address: Address, to: Address, value: Union[int, float],
                                         valid_after: Uint256, valid_before: Uint256, nonce: Bytes32,
                                         v: Uint8, r: Bytes32, s: Bytes32) -> HexBytes:
        """
        Execute a signed transfer
        
        Args:
            from_address: Sender address
            to: Recipient address
            value: Amount to transfer
            valid_after: Starting validity timestamp
            valid_before: Ending validity timestamp
            nonce: Unique nonce
            v: Signature v parameter
            r: Signature r parameter
            s: Signature s parameter
            
        Returns:
            HexBytes: Transaction hash
        """
        ...
    
    async def receive_with_authorization(self, from_address: Address, to: Address, value: Union[int, float],
                                        valid_after: Uint256, valid_before: Uint256, nonce: Bytes32,
                                        v: Uint8, r: Bytes32, s: Bytes32) -> HexBytes:
        """
        Execute a signed receive
        
        Args:
            from_address: Sender address
            to: Recipient address
            value: Amount to transfer
            valid_after: Starting validity timestamp
            valid_before: Ending validity timestamp
            nonce: Unique nonce
            v: Signature v parameter
            r: Signature r parameter
            s: Signature s parameter
            
        Returns:
            HexBytes: Transaction hash
        """
        ...
    
    async def cancel_authorization(self, authorizer: Address, nonce: Bytes32,
                                 v: Uint8, r: Bytes32, s: Bytes32) -> HexBytes:
        """
        Cancel a signed authorization
        
        Args:
            authorizer: Authorizer address
            nonce: Authorization nonce
            v: Signature v parameter
            r: Signature r parameter
            s: Signature s parameter
            
        Returns:
            HexBytes: Transaction hash
        """
        ...