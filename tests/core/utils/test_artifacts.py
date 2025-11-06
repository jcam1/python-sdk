import pytest

from packages.core.jpyc_core_sdk.utils.artifacts import (
    get_artifacts,
    resolve_artifacts_file_path,
)


@pytest.mark.parametrize(
    [
        "contract_type",
    ],
    [
        pytest.param(
            "jpyc",
            id="file path for artifacts of jpyc contract",
        ),
        pytest.param(
            "jpyc_prepaid",
            id="file path for artifacts of jpyc_prepaid contract",
        ),
    ],
)
def test_resolve_artifacts_file_path(contract_type):
    path = resolve_artifacts_file_path(contract_type=contract_type)
    assert str(path).endswith(f"{contract_type}.json") is True


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
    path = resolve_artifacts_file_path(contract_type="jpyc")

    artifact = get_artifacts(file_path=path, artifact_type=artifact_type)
    assert type(artifact) is return_type
