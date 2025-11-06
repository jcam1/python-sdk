import json
from pathlib import Path
from typing import Any

from .types import ArtifactType, ContractType


def resolve_artifacts_file_path(contract_type: ContractType) -> Path:
    """Resolve the path of artifacts file from the specified contract type.

    Args:
        contract_type (ContractType): Contract type

    Returns:
        Path: Absolute path of artifacts file
    """
    path = Path(__file__).parent.parent.joinpath("artifacts", f"{contract_type}.json")

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
