from importlib.metadata import version

from .client import SdkClient
from .jpyc import JPYC

__version__ = version("jpyc-core-sdk")
__all__ = [
    "__version__",
    "SdkClient",
    "JPYC",
]
