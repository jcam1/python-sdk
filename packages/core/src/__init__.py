from importlib.metadata import version

from core.src.client import *
from core.src.jpyc import *

__version__ = version("jpyc-core-sdk")
__all__ = [
    "__version__",
    "SdkClient",
    "JPYC",
]
