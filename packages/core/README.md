# Core SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![build](https://github.com/jcam1/python-sdk/actions/workflows/check.yml/badge.svg)

Python SDK to interact with [the JPYCv2's core contracts](https://github.com/jcam1/JPYCv2/blob/main/contracts/v1/FiatTokenV1.sol). Ideal for those who want to interact with JPYC protocol in any Python-backend environments.

## 🪄 Usage

First, configure clients for the SDK.

```py
from jpyc-core-sdk.client import SdkClient
from jpyc-core-sdk.jpyc import JPYC

# Configure SDK client using default RPC endpoint
client = SdkClient(
    chain_name="ethereum",
    network_name="mainnet",
    private_key={PRIVATE_KEY},
)

# Or configure SDK client using custom RPC endpoint
client = SdkClient(
    chain_name="ethereum",
    network_name="mainnet",
    private_key={PRIVATE_KEY},
    rpc_endpoint={CUSTOM_RPC_ENDPOINT},
)

# Configure JPYC client
jpyc = JPYC(client=client)
```

Then, use the configured JPYC client to call JPYC's contract functions wherever you would like.

```py
from {CONFIG_FILE} import jpyc

# Call a contract function (e.g., transfer)
jpyc.transfer(
    to={TO_ADDRESS},
    value=2025,
)
```

> [!NOTE]  
> More code examples are available at [`examples` directory](./examples/).
> More detailed development documentation is available at [`docs` directory](../../docs/core/).

## ⛓️ Supported Networks

Please use one of the combinations of chain-network names when configuring the SDK clients.

> [!TIP]
> For local testing & development, you could use `localhost`-`devnet` pair.

|  Chain Name | Network Names        |
| ----------: | :------------------- |
|  `ethereum` | `mainnet`, `sepolia` |
|   `polygon` | `mainnet`, `amoy`    |
|    `gnosis` | `mainnet`, `chiado`  |
| `avalanche` | `mainnet`, `fuji`    |
|     `astar` | `mainnet`            |
|    `shiden` | `mainnet`            |
| `localhost` | `devnet`             |

## 💬 Supported Providers

**We're currently supporting `HTTPProvider` (the most simple & widely-used one) only.** More providers (notably `WebSocketProvider`) are to be supported in the near future, so stay tuned!

## 🛠 Development

> [!IMPORTANT]
> Sections below are mainly for the advanced users (e.g., contributors of this repo).

### 📦 Package Management

#### Add packages

```sh
# add packages for production
$ uv add {package_name}
# add packages for development
$ uv add --dev {package_name}
```

#### Remove packages

```sh
# remove production packages
$ uv remove {package_name}
# remove development packages
$ uv remove --dev {package_name}
```

### 🔎 Testing

Please see [`README` at `tests` directory](../../tests/README.md).

### ✅ Static Code Analysis

#### Linting

```sh
# run linter without fixing
$ uv run riff check {dir_name}
# run linter & auto-fix (if available)
$ uv run riff check {dir_name} --fix
```

#### Formatting

```sh
# run formatter without fixing
$ uv run riff format {dir_name} --check
# run formatter & auto-fix
$ uv run riff format {dir_name}
```

#### Type Checking

```sh
# run mypy
$ uv run mypy {dir_name}
```

#### Pre-Commit Hooks

Pre-commit script is configured at [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml). This automatically runs the configured hooks before executing any `git commit` commands. You could also simulate the hooks by running the following.

```sh
# simulate pre-commit hooks without creating an actual commit
$ uv run pre-commit run --all-files
```

### 📝 Comments & Docstrings

Docstrings should be written in [the Google-style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
