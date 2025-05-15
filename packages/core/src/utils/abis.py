import json
from pathlib import Path
from typing import Any

from core.src.utils.types import ContractVersion

def resolve_abi_file_path(contract_version: ContractVersion) -> str:
    """Resolve the path of ABI file from the specified contract version.

    Args:
        version (ContractVersion): Contract version

    Returns:
        str: Absolute path of ABI file
    """
    path = Path(__file__).parent.parent.joinpath("abis", f"v{contract_version}.json")

    return path.absolute()

def get_abi(file_path: str) -> Any:
    """Get ABI from the specified path.

    Args:
        file_path (str): absolute path of ABI file

    Returns:
        Any: Contents of ABI
    """
    with open(file_path) as f:
        return json.load(f)
