from typing import Final

########
# Math #
########

UINT_MIN: Final[int] = 0
"""int: Minimum value of uint."""
UINT8_MAX: Final[int] = 255
"""int: Maximum value of uint8."""
UINT256_MAX: Final[int] = 115792089237316195423570985008687907853269984665640564039457584007913129639935
"""int: Maximum value of uint256."""

####################
# Middleware Names #
####################

POA_MIDDLEWARE: Final[str] = "poa_middleware"
"""str: Name of POA compatibility middleware."""
SIGN_MIDDLEWARE: Final[str] = "sign_middleware"
"""str: Name of auto-signature middleware."""
