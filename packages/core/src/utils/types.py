from typing import Literal, TypeAlias, TypedDict

##########
# Chains #
##########

ChainName: TypeAlias = Literal[
    "ethereum",
    "polygon",
    "gnosis",
    "avalanche",
    "astar",
    "shiden",
    "local",
]


class NetworkMetadata(TypedDict):
    id: int
    name: str
    rpc_endpoints: list[str]


ChainMetadata: TypeAlias = dict[ChainName, dict[str, NetworkMetadata]]
"""A type that contains metadata of chains."""

#############
# Contracts #
#############

ContractVersion: TypeAlias = Literal["2"]
"""A type that contains available contract versions."""
ArtifactType: TypeAlias = Literal["abi", "bytecode"]
"""A type that contains types of contract artifacts."""
