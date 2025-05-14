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

#############
# Contracts #
#############

ContractVersion: TypeAlias = Literal["2"]
