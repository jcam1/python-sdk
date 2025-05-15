from .errors import (
    AccountNotInitialized,
    TransactionFailedToSend,
    TransactionSimulationFailed,
)

def catch_transaction_errors(func):
    """Decorator to catch any transaction errors.

    Raises:
        AccountNotInitialized: If account is not initialized
        TransactionFailedToSend: If failed to send a transaction
    """
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AccountNotInitialized:
            raise AccountNotInitialized()
        except TransactionSimulationFailed as e:
            raise TransactionSimulationFailed(e)
        except Exception as e:
            raise TransactionFailedToSend(e)

    return wrapper
