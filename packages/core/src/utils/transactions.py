from .errors import TransactionFailed

def catch_transaction_errors(func):
    """Decorator to catch transaction errors."""
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            raise TransactionFailed(e)

    return wrapper
