from importlib.metadata import version

from .client import *
from .jpyc import *

__version__ = version("jpyc-core-sdk")
__all__ = [
    "__version__",
    "SdkClient",
    "JPYC",
]
