import json
from pathlib import Path
from typing import Any

from .types import ArtifactType, ContractVersion

def resolve_artifacts_file_path(contract_version: ContractVersion) -> str:
    """Resolve the path of artifacts file from the specified contract version.

    Args:
        version (ContractVersion): Contract version

    Returns:
        str: Absolute path of artifacts file
    """
    path = Path(__file__).parent.parent.parent.joinpath("artifacts", f"v{contract_version}.json")

    return path.absolute()

def get_artifacts(file_path: str, artifact_type: ArtifactType) -> Any:
    """Get contract artifacts from the specified file path.

    Args:
        file_path (str): absolute path of artifacts file

    Returns:
        Any: Artifacts of contracts
    """
    with open(file_path) as f:
        return json.load(f)[artifact_type]
