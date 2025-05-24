import json
from pathlib import Path
from typing import Any

from .types import ArtifactType, ContractVersion


def resolve_artifacts_file_path(contract_version: ContractVersion) -> Path:
    """Resolve the path of artifacts file from the specified contract version.

    Args:
        contract_version (ContractVersion): Contract version

    Returns:
        Path: Absolute path of artifacts file
    """
    path = Path(__file__).parent.parent.parent.joinpath(
        "artifacts", f"v{contract_version}.json"
    )

    return path.absolute()


def get_artifacts(file_path: Path, artifact_type: ArtifactType) -> Any:
    """Get contract artifacts from the specified file path.

    Args:
        file_path (Path): absolute path of artifacts file
        artifact_type (ArtifactType): type of artifacts

    Returns:
        Any: Artifacts of contracts
    """
    with open(file_path) as f:
        return json.load(f)[artifact_type]
