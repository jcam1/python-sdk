# JPYC SDK Python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/jcam1/python-sdks/issues/new/choose)

Python SDK for JPYC

## 🌈 SDK Overview

This SDK provides Python interfaces to interact with JPYCv2 smart contracts on different chains. Currently, we support Ethereum, Polygon, Gnosis, Avalanche, Astar, and Shiden.

## 📦 Package Structure

Unlike the Node.js version which uses a monorepo structure with multiple packages (core and potentially others), this Python SDK has been designed as a single package for simplicity and to follow Python packaging conventions.

This approach simplifies installation, dependency management, and usage while still providing the same functionality. If the project grows significantly in the future, we could consider splitting it into multiple packages using a tool like Poetry's namespace packages.

## 💡 Usage

Please follow the following steps to configure SDK.

### 1. Installation

Install the package using Poetry or pip.

```bash
# Using Poetry
$ poetry add jpyc-sdk-python
```

```bash
# Using pip
$ pip install jpyc-sdk-python
```

### 2. Environment Variables

Some data, such as configuration variables (e.g., chain name) or sensitive data (e.g., private key), are embedded as environment variables. You need to set the following environment variables.

|              Variable | Description & Instructions                                                                                                        |
| --------------------: | :-------------------------------------------------------------------------------------------------------------------------------- |
|             `SDK_ENV` | SDK environment. Set to `local` for local environment or any other sensible name for production environment.                      |
|          `CHAIN_NAME` | Chain name. Set to one of the following\: `local`, `ethereum`, `polygon`, `gnosis`, `avalanche`, `astar` or `shiden`.             |
|        `NETWORK_NAME` | Network name within the specified chain. Set to one of the following\: `mainnet`, `goerli`, `sepolia`, `amoy`, `chiado` or `fuji` |
|        `RPC_ENDPOINT` | RPC endpoint to send transactions.                                                                                                |
|         `PRIVATE_KEY` | Private key of an account.                                                                                                        |
| `LOCAL_PROXY_ADDRESS` | Proxy contract address in local environment.                                                                                      |

### 3. SDK Instantiation

Initialize an SDK instance.

```python
from jpyc_sdk import SdkClient, JPYC
from jpyc_sdk.types import ChainName, NetworkName
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. Initialize an SdkClient instance
sdk_client = SdkClient(
    chain_name=os.getenv("CHAIN_NAME"),
    network_name=os.getenv("NETWORK_NAME"),
    rpc_endpoint=os.getenv("RPC_ENDPOINT")
)

# 2. Generate an account from a private key
account = sdk_client.create_private_key_account()

# 3. Generate a client with the account
client = sdk_client.create_local_client(account=account)

# 4. Initialize an SDK instance
jpyc = JPYC(client=client)
```

### 4. SDK Usage

Use the initialized SDK wherever you would like.

```python
from your.path.to.initialization.file import jpyc

# Fetch `totalSupply` from `JPYCv2` contract
total_supply = jpyc.total_supply()
print(f"totalSupply: {total_supply}")
```

## 🤖 Available Commands

The following commands are available for local development & testing.

|          Command | Description                                 |
| ---------------: | :------------------------------------------ |
|           `test` | Run tests (using pytest)                    |
|           `lint` | Run linters (mypy/black)                    |
|          `build` | Build the SDK                               |
|          `clean` | Clean build files                           |
|           `docs` | Generate documentation (Markdown/HTML)      |
|        `docs-md` | Generate documentation in Markdown format   |
|      `docs-html` | Generate documentation in HTML format       |

These commands can be run as follows:

```bash
# Run tests
$ poetry run pytest

# Run linters
$ poetry run black jpyc_sdk tests
$ poetry run mypy jpyc_sdk

# Generate documentation
$ poetry run docs
```

## 🔥 How to Contribute

We appreciate your interest to contribute to this project! Please follow these steps to contribute:

### 1. Create an Issue

The first thing to do is to create a new issue. Feel free to create new issues from [here](https://github.com/jcam1/python-sdk/issues/new/choose) to propose/request new features or report bugs.

### 2. Clone This Repository

Next, clone this repo. Our default branch is `develop`.

```bash
$ git clone https://github.com/yourusername/jpyc-sdk-python.git
```

### 3. Checkout to a New Branch

You then need to checkout to a new branch (name whatever you would like) from the cloned `develop` branch.

```bash
$ git checkout -b ${your_branch_name}
```

### 4. Write Code

Now, write code to implement the proposed features and/or to fix bugs.

### 5. Open a Pull Request

Finally, open a new PR from your branch to `develop` branch, and describe what you'll have done.

## 📚 Documentation

You can find the auto-generated developer documentation [here](https://jcam1.github.io/python-sdk/).
