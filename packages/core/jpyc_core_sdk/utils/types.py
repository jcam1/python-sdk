from typing import Literal, TypedDict

from web3.contract.contract import ContractFunction

##########
# Chains #
##########

type ChainName = Literal[
    "ethereum",
    "polygon",
    "gnosis",
    "avalanche",
    "astar",
    "shiden",
    "localhost",
]


class NetworkMetadata(TypedDict):
    id: int
    name: str
    rpc_endpoints: list[str]


type ChainMetadata = dict[ChainName, dict[str, NetworkMetadata]]
"""A type that contains metadata of chains."""

#############
# Contracts #
#############

type ContractVersion = Literal["2"]
"""A type that contains available contract versions."""
type ArtifactType = Literal["abi", "bytecode"]
"""A type that contains types of contract artifacts."""

################
# Transactions #
################


class TransactionArgs(TypedDict):
    contract_func: ContractFunction
    func_args: dict[str, object]
