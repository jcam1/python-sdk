from typing import List, Literal, TypeAlias, TypedDict

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
    rpc_endpoints: List[str]

ChainMetadata: TypeAlias = dict[ChainName, dict[str, NetworkMetadata]]

#############
# Contracts #
#############

ContractVersion: TypeAlias = Literal["2"]
