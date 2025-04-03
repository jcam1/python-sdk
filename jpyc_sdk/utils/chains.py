"""Chain and network configuration module

This module provides definitions of blockchains and networks supported by the JPYC SDK,
as well as utility functions for working with them.
It includes functionality for validating supported chains and networks, and configuring Web3 instances.
"""

from typing import Dict, Any, List
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

from .types import ChainName, NetworkName

# Chain and network definitions
SUPPORTED_CHAINS = {
    "local": {
        "mainnet": {
            "id": 31337,
            "name": "Hardhat",
            "native_currency": {
                "name": "Ether",
                "symbol": "ETH",
                "decimals": 18
            },
            "rpc_urls": ["http://127.0.0.1:8545/"]
        }
    },
    "ethereum": {
        "mainnet": {
            "id": 1,
            "name": "Ethereum Mainnet",
            "native_currency": {
                "name": "Ether",
                "symbol": "ETH",
                "decimals": 18
            },
            "rpc_urls": ["https://ethereum.publicnode.com"]
        },
        "goerli": {
            "id": 5,
            "name": "Goerli Testnet",
            "native_currency": {
                "name": "Goerli Ether",
                "symbol": "ETH",
                "decimals": 18
            },
            "rpc_urls": ["https://goerli.infura.io/v3/"]
        },
        "sepolia": {
            "id": 11155111,
            "name": "Sepolia Testnet",
            "native_currency": {
                "name": "Sepolia Ether",
                "symbol": "ETH",
                "decimals": 18
            },
            "rpc_urls": ["https://sepolia.infura.io/v3/"]
        }
    },
    "polygon": {
        "mainnet": {
            "id": 137,
            "name": "Polygon Mainnet",
            "native_currency": {
                "name": "MATIC",
                "symbol": "MATIC",
                "decimals": 18
            },
            "rpc_urls": ["https://polygon-rpc.com"]
        },
        "amoy": {
            "id": 80002,
            "name": "Polygon Amoy Testnet",
            "native_currency": {
                "name": "MATIC",
                "symbol": "MATIC",
                "decimals": 18
            },
            "rpc_urls": ["https://rpc-amoy.polygon.technology"]
        }
    },
    "gnosis": {
        "mainnet": {
            "id": 100,
            "name": "Gnosis Chain",
            "native_currency": {
                "name": "xDAI",
                "symbol": "xDAI",
                "decimals": 18
            },
            "rpc_urls": ["https://rpc.gnosischain.com"]
        },
        "chiado": {
            "id": 10200,
            "name": "Chiado Testnet",
            "native_currency": {
                "name": "xDAI",
                "symbol": "xDAI",
                "decimals": 18
            },
            "rpc_urls": ["https://rpc.chiadochain.net"]
        }
    },
    "avalanche": {
        "mainnet": {
            "id": 43114,
            "name": "Avalanche C-Chain",
            "native_currency": {
                "name": "Avalanche",
                "symbol": "AVAX",
                "decimals": 18
            },
            "rpc_urls": ["https://api.avax.network/ext/bc/C/rpc"]
        },
        "fuji": {
            "id": 43113,
            "name": "Avalanche Fuji Testnet",
            "native_currency": {
                "name": "Avalanche",
                "symbol": "AVAX",
                "decimals": 18
            },
            "rpc_urls": ["https://api.avax-test.network/ext/bc/C/rpc"]
        }
    },
    "astar": {
        "mainnet": {
            "id": 592,
            "name": "Astar Network",
            "native_currency": {
                "name": "Astar",
                "symbol": "ASTR",
                "decimals": 18
            },
            "rpc_urls": ["https://astar.public.blastapi.io"]
        }
    },
    "shiden": {
        "mainnet": {
            "id": 336,
            "name": "Shiden Network",
            "native_currency": {
                "name": "Shiden",
                "symbol": "SDN",
                "decimals": 18
            },
            "rpc_urls": ["https://shiden.public.blastapi.io"]
        }
    }
}

def get_supported_chain_names() -> List[str]:
    """
    Get a list of supported chain names.
    
    Returns:
        List[str]: List of supported chain names
    """
    return list(SUPPORTED_CHAINS.keys())

def is_valid_chain_name(chain_name: str) -> bool:
    """
    Check if the specified chain name is supported.
    
    Args:
        chain_name: Chain name to check
        
    Returns:
        bool: True if supported, False otherwise
    """
    return chain_name in SUPPORTED_CHAINS

def get_supported_network_names(chain_name: str) -> List[str]:
    """
    Get a list of supported network names for the specified chain.
    
    Args:
        chain_name: Chain name
        
    Returns:
        List[str]: List of supported network names
    """
    if chain_name in SUPPORTED_CHAINS:
        return list(SUPPORTED_CHAINS[chain_name].keys())
    return []

def is_valid_network_name(chain_name: str, network_name: str) -> bool:
    """
    Check if the specified network name is supported for the specified chain.
    
    Args:
        chain_name: Chain name
        network_name: Network name
        
    Returns:
        bool: True if supported, False otherwise
    """
    return chain_name in SUPPORTED_CHAINS and network_name in SUPPORTED_CHAINS[chain_name]

def get_web3_for_chain(chain_name: ChainName, network_name: NetworkName, rpc_endpoint: str) -> Web3:
    """
    Get a Web3 instance configured for the specified chain and network.
    
    Args:
        chain_name: Chain name
        network_name: Network name
        rpc_endpoint: RPC endpoint URL
        
    Returns:
        Web3: Configured Web3 instance
    """
    web3 = Web3(Web3.HTTPProvider(rpc_endpoint))
    
    # Add POA middleware for chains that require it
    poa_chains = ["goerli", "sepolia", "polygon", "gnosis"]
    if chain_name in poa_chains or (chain_name == "ethereum" and network_name in ["goerli", "sepolia"]):
        web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    
    return web3