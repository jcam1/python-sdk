from abc import ABC, abstractmethod
from decimal import Decimal

from eth_typing import ChecksumAddress

class IJPYC(ABC):
    """Interface of JPYC contracts."""

    ##################
    # View functions #
    ##################

    @abstractmethod
    def is_minter(self, account: ChecksumAddress) -> bool:
        """Call `isMinter` function.

        Args:
            account (ChecksumAddress): Account address

        Returns:
            bool: True if `account` is a minter, false otherwise
        """
        pass

    @abstractmethod
    def minter_allowance(self, minter: ChecksumAddress) -> Decimal:
        """Call `minterAllowance` function.

        Args:
            minter (ChecksumAddress): Minter address

        Returns:
            Decimal: Minter allowance
        """
        pass

    @abstractmethod
    def total_supply(self) -> Decimal:
        """Call `totalSupply` function.

        Returns:
            Decimal: Total supply of tokens
        """
        pass

    @abstractmethod
    def balance_of(self, account: ChecksumAddress) -> Decimal:
        """Call `balanceOf` function.

        Args:
            account (ChecksumAddress): Account address

        Returns:
            Decimal: Account balance
        """
        pass

    @abstractmethod
    def allowance(self, owner: ChecksumAddress, spender: ChecksumAddress) -> Decimal:
        """Call `allowance` function.

        Args:
            owner (ChecksumAddress): Owner address
            spender (ChecksumAddress): Spender address

        Returns:
            Decimal: Allowance of spender over owner's tokens
        """
        pass

    @abstractmethod
    def nonces(self, owner: ChecksumAddress) -> int:
        """Call `nonces` function.

        Args:
            owner (ChecksumAddress): Owner address

        Returns:
            int: Nonce for EIP2612's `permit`.
        """
        pass

    ######################
    # Mutation functions #
    ######################

    @abstractmethod
    def configure_minter(self, minter: ChecksumAddress, minter_allowed_amount: Decimal) -> str:
        """Call `configureMinter` function.

        Args:
            minter (ChecksumAddress): Minter address
            minter_allowed_amount (Decimal): Minter allowance

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def mint(self, to: ChecksumAddress, amount: Decimal) -> str:
        """Call `mint` function.

        Args:
            to (ChecksumAddress): Receiver address
            amount (Decimal): Amount of tokens to mint

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def transfer(self, to: ChecksumAddress, value: Decimal) -> str:
        """Call `transfer` function.

        Args:
            to (ChecksumAddress): Receiver address
            value (Decimal): Amount of tokens to transfer

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def transfer_from(self, from_: ChecksumAddress, to: ChecksumAddress, value: Decimal) -> str:
        """Call `transferFrom` function.

        Args:
            from_ (ChecksumAddress): Owner address
            to (ChecksumAddress): Receiver address
            value (Decimal): Amount of tokens to transfer

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
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
        """Call `transferWithAuthorization` function.

        Args:
            from_ (ChecksumAddress): Owner address
            to (ChecksumAddress): Receiver allowance
            value (Decimal): Amount of tokens to transfer
            validAfter (int): Unix time when transaction becomes valid
            validBefore (int): Unix time when transaction becomes invalid
            nonce (str): Unique nonce
            v (int): v of ECDSA
            r (str): r of ECDSA
            s (str): s of ECDSA

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
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
        """Call `receiveWithAuthorization` function.

        Args:
            from_ (ChecksumAddress): Owner address
            to (ChecksumAddress): Receiver allowance
            value (Decimal): Amount of tokens to transfer
            validAfter (int): Unix time when transaction becomes valid
            validBefore (int): Unix time when transaction becomes invalid
            nonce (str): Unique nonce
            v (int): v of ECDSA
            r (str): r of ECDSA
            s (str): s of ECDSA

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def cancel_authorization(
        self,
        authorizer: ChecksumAddress,
        nonce: str,
        v: int,
        r: str,
        s: str,
    ) -> str:
        """Call `cancelAuthorization` function.

        Args:
            authorizer (ChecksumAddress): Owner address
            nonce (str): Unique nonce
            v (int): v of ECDSA
            r (str): r of ECDSA
            s (str): s of ECDSA

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def approve(self, spender: ChecksumAddress, value: Decimal) -> str:
        """Call `approve` function.

        Args:
            spender (ChecksumAddress): Spender address
            value (Decimal): Amount of allowance

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def increase_allowance(self, spender: ChecksumAddress, increment: Decimal) -> str:
        """Call `increaseAllowance` function.

        Args:
            spender (ChecksumAddress): Spender address
            increment (Decimal): Amount of allowance to increase

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def decrease_allowance(self, spender: ChecksumAddress, decrement: Decimal) -> str:
        """Call `decreaseAllowance` function.

        Args:
            spender (ChecksumAddress): Spender address
            decrement (Decimal): Amount of allowance to decrease

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
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
        """Call `permit` function.

        Args:
            owner (ChecksumAddress): Owner address
            spender (ChecksumAddress): Spender address
            value (Decimal): Amount of allowance
            deadline (int): Unix time when transaction becomes invalid
            v (int): v of ECDSA
            r (str): r of ECDSA
            s (str): s of ECDSA

        Returns:
            str: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass
