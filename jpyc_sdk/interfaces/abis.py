"""
ABI (Application Binary Interface) definitions for JPYC contracts
"""

import json
import pathlib

package_dir = pathlib.Path(__file__).parent.parent
abi_file = package_dir / "artifacts" / "JPYCv2" / "contracts" / "v1" / "FiatTokenV1.sol" / "FiatTokenV1.json"

with open(abi_file, 'r') as f:
    JPYC_V2_ABI = json.load(f)['abi']