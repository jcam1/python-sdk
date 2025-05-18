from abc import ABC, abstractmethod

from utils.validators import Bytes32, ChecksumAddress, Uint256, Uint8

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
    def minter_allowance(self, minter: ChecksumAddress) -> Uint256:
        """Call `minterAllowance` function.

        Args:
            minter (ChecksumAddress): Minter address

        Returns:
            Decimal: Minter allowance
        """
        pass

    @abstractmethod
    def total_supply(self) -> Uint256:
        """Call `totalSupply` function.

        Returns:
            Decimal: Total supply of tokens
        """
        pass

    @abstractmethod
    def balance_of(self, account: ChecksumAddress) -> Uint256:
        """Call `balanceOf` function.

        Args:
            account (ChecksumAddress): Account address

        Returns:
            Decimal: Account balance
        """
        pass

    @abstractmethod
    def allowance(self, owner: ChecksumAddress, spender: ChecksumAddress) -> Uint256:
        """Call `allowance` function.

        Args:
            owner (ChecksumAddress): Owner address
            spender (ChecksumAddress): Spender address

        Returns:
            Decimal: Allowance of spender over owner's tokens
        """
        pass

    @abstractmethod
    def nonces(self, owner: ChecksumAddress) -> Uint256:
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
    def configure_minter(self, minter: ChecksumAddress, minter_allowed_amount: Uint256) -> Bytes32:
        """Call `configureMinter` function.

        Args:
            minter (ChecksumAddress): Minter address
            minter_allowed_amount (Uint256): Minter allowance

        Returns:
            Bytes32: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def mint(self, to: ChecksumAddress, amount: Uint256) -> Bytes32:
        """Call `mint` function.

        Args:
            to (ChecksumAddress): Receiver address
            amount (Uint256): Amount of tokens to mint

        Returns:
            Bytes32: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def transfer(self, to: ChecksumAddress, value: Uint256) -> Bytes32:
        """Call `transfer` function.

        Args:
            to (ChecksumAddress): Receiver address
            value (Uint256): Amount of tokens to transfer

        Returns:
            Bytes32: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def transfer_from(self, from_: ChecksumAddress, to: ChecksumAddress, value: Uint256) -> Bytes32:
        """Call `transferFrom` function.

        Args:
            from_ (ChecksumAddress): Owner address
            to (ChecksumAddress): Receiver address
            value (Uint256): Amount of tokens to transfer

        Returns:
            Bytes32: Transaction hash

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
        value: Uint256,
        valid_after: Uint256,
        valid_before: Uint256,
        nonce: Bytes32,
        v: Uint8,
        r: Bytes32,
        s: Bytes32,
    ) -> Bytes32:
        """Call `transferWithAuthorization` function.

        Args:
            from_ (ChecksumAddress): Owner address
            to (ChecksumAddress): Receiver allowance
            value (Uint256): Amount of tokens to transfer
            valid_after (Uint256): Unix time when transaction becomes valid
            valid_before (Uint256): Unix time when transaction becomes invalid
            nonce (Bytes32): Unique nonce
            v (Uint8): v of ECDSA
            r (Bytes32): r of ECDSA
            s (Bytes32): s of ECDSA

        Returns:
            Bytes32: Transaction hash

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
        value: Uint256,
        valid_after: Uint256,
        valid_before: Uint256,
        nonce: Bytes32,
        v: Uint8,
        r: Bytes32,
        s: Bytes32,
    ) -> Bytes32:
        """Call `receiveWithAuthorization` function.

        Args:
            from_ (ChecksumAddress): Owner address
            to (ChecksumAddress): Receiver allowance
            value (Uint256): Amount of tokens to transfer
            valid_after (Uint256): Unix time when transaction becomes valid
            valid_before (Uint256): Unix time when transaction becomes invalid
            nonce (Bytes32): Unique nonce
            v (Uint8): v of ECDSA
            r (Bytes32): r of ECDSA
            s (Bytes32): s of ECDSA

        Returns:
            Bytes32: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def cancel_authorization(
        self,
        authorizer: ChecksumAddress,
        nonce: Bytes32,
        v: Uint8,
        r: Bytes32,
        s: Bytes32,
    ) -> Bytes32:
        """Call `cancelAuthorization` function.

        Args:
            authorizer (ChecksumAddress): Owner address
            nonce (Bytes32): Unique nonce
            v (Uint8): v of ECDSA
            r (Bytes32): r of ECDSA
            s (Bytes32): s of ECDSA

        Returns:
            Bytes32: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def approve(self, spender: ChecksumAddress, value: Uint256) -> Bytes32:
        """Call `approve` function.

        Args:
            spender (ChecksumAddress): Spender address
            value (Uint256): Amount of allowance

        Returns:
            Bytes32: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def increase_allowance(self, spender: ChecksumAddress, increment: Uint256) -> Bytes32:
        """Call `increaseAllowance` function.

        Args:
            spender (ChecksumAddress): Spender address
            increment (Uint256): Amount of allowance to increase

        Returns:
            Bytes32: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass

    @abstractmethod
    def decrease_allowance(self, spender: ChecksumAddress, decrement: Uint256) -> Bytes32:
        """Call `decreaseAllowance` function.

        Args:
            spender (ChecksumAddress): Spender address
            decrement (Uint256): Amount of allowance to decrease

        Returns:
            Bytes32: Transaction hash

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
        value: Uint256,
        deadline: Uint256,
        v: Uint8,
        r: Bytes32,
        s: Bytes32,
    ) -> Bytes32:
        """Call `permit` function.

        Args:
            owner (ChecksumAddress): Owner address
            spender (ChecksumAddress): Spender address
            value (Uint256): Amount of allowance
            deadline (Uint256): Unix time when transaction becomes invalid
            v (Uint8): v of ECDSA
            r (Bytes32): r of ECDSA
            s (Bytes32): s of ECDSA

        Returns:
            Bytes32: Transaction hash

        Raises:
            AccountNotInitialized: If account is not initialized
            TransactionFailedToSend: If failed to send a transaction
        """
        pass
