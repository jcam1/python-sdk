# JPYC Python SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/jcam1/python-sdk/issues/new/choose)

=> 英語版は[こちら](./README.md)。

## 💫 利用可能な SDK

各 SDK に関する詳細は、それぞれの `README` を参照ください。

|            SDK 名 | `README`                                   |
| --------------: | :----------------------------------------- |
| `jpyc-core-sdk` | [packages/core](./packages/core/README.md) |

## ⬇️ インストール

### 1. リポジトリのクローン

```sh
# リポジトリのクローン
$ git clone https://github.com/jcam1/python-sdk.git
# `python-sdk`ディレクトリへの移動
$ cd python-sdk
```

### 2. `uv` のインストール

このリポジトリでは、パッケージ管理ツールとして `uv` を利用しています。デバイスにインストールされていない場合は、[uv 公式ドキュメント](https://docs.astral.sh/uv/getting-started/installation/)に沿って各種ダウンロード・インストールを進めてください。例として、以下のコマンドは MacOS 上に `uv` をインストールします。

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. パッケージのインストール

```sh
uv sync
```

## 💪🏻 コントリビューションを検討されている方へ

詳細は [CONTRIBUTING.md](./CONTRIBUTING.md) を参照してください。
