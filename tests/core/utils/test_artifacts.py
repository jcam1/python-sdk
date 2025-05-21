import pytest

from packages.core.src.utils.artifacts import (
    get_artifacts,
    resolve_artifacts_file_path,
)


def test_resolve_artifacts_file_path():
    path = resolve_artifacts_file_path(contract_version="2")
    assert str(path).endswith("v2.json") is True


@pytest.mark.parametrize(
    [
        "artifact_type",
        "return_type",
    ],
    [
        pytest.param(
            "abi",
            list,
            id="get abi",
        ),
        pytest.param(
            "bytecode",
            str,
            id="get bytecode",
        ),
    ],
)
def test_get_artifacts(artifact_type, return_type):
    path = resolve_artifacts_file_path(contract_version="2")

    artifact = get_artifacts(file_path=path, artifact_type=artifact_type)
    assert type(artifact) is return_type
