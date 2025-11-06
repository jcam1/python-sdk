# JPYC Core SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![build](https://github.com/jcam1/python-sdk/actions/workflows/check.yml/badge.svg)

JPYC Python SDK は、各ネットワーク上にデプロイされた JPYC コントラクトとやりとりをするための Python インターフェースです。=> 英語版は[こちら](./README.md)。

## ✅ 対応しているコントラクト種別・ネットワーク

この SDK は2025年10月現在、以下のコントラクト種別とネットワークに対応しています。SDK クライアントを設定する際は、以下のいずれかのチェーン名・ネットワーク名の組み合わせを指定してください。

> [!NOTE]
> 以下のネットワーク以外にも、ローカルネットワーク（チェーン名: `localhost`・ネットワーク名: `devnet`）にデプロイした JPYC コントラクトのアドレスを設定して、ローカル環境での開発や検証に使うこともできます。

> [!IMPORTANT]
> この SDK は2025年10月現在、`HTTPプロバイダー`のみに対応しています。他プロバイダー（e.g., `WebSocketプロバイダー`）への対応も計画中ですので、定期的にこのリポジトリーを確認することをお勧めします。

|                               | JPYC | JPYC Prepaid | チェーン名 | ネットワーク名 |
| ----------------------------: | :--: | :----------: |  :----------: |  :----------: |
|         Ethereum メインネット |  ✅  |      ✅      |  `ethereum` | `mainnet` |
| Ethereum Sepolia テストネット |  ✅  |      ✅      | `ethereum` | `sepolia` |
|      Polygon PoS メインネット |  ✅  |      ✅      | `polygon` | `mainnet` |
|     Polygon Amoy テストネット |  ✅  |      ✅      | `polygon` | `amoy` |
|        Avalanche メインネット |  ✅  |      ✅      | `avalanche` | `mainnet` |
|   Avalanche Fuji テストネット |  ✅  |      ✅      | `avalanche` | `fuji` |

## 🪄 使い方

### 1. `jpyc-core-sdk` パッケージのインストール

```sh
# uv
$ uv add jpyc-core-sdk
# poetry
$ poetry add jpyc-core-sdk
# pip
$ pip install jpyc-core-sdk
```

### 2. SDK クラアントの設定

```py
from jpyc_core_sdk import JPYC, SdkClient

# デフォルトのRPCエンドポイントを用いた設定例
client = SdkClient(
    chain_name="polygon",
    network_name="mainnet",
    private_key={PRIVATE_KEY},
)

# 独自のRPCエンドポイントを用いた設定例
client = SdkClient(
    chain_name="polygon",
    network_name="mainnet",
    private_key={PRIVATE_KEY},
    rpc_endpoint={CUSTOM_RPC_ENDPOINT},
)

# JPYCクライアントの初期化
jpyc = JPYC(client=client)
```

> [!TIP]
> SDK の内部では設計上の観点から環境変数を用いていません。一方で、アプリケーション側から SDK に対して秘匿性の高いデータ（e.g., プライベートキー）を渡す際には、ハードコードせず、環境変数を使用するなどの考慮が別途必要です。

### 3. JPYC コントラクトの呼び出し

ステップ 2 で初期化した JPYC クライアントを用いて、Python アプリケーション内で、任意の JPYC コントラクト関数を呼び出すことができます。

```py
from {CONFIG_FILE} import jpyc

...
# `transfer`関数の呼び出し
tx_hash = jpyc.transfer(
    to={TO_ADDRESS},
    value=2025,
)
...
```

## ✨ 実装例

[`examples`ディレクトリ](./examples/)に SDK を使ったコードの実装例を多数用意しています。ディレクトリ内の `README` にしたがって、サンプルコードを実行するための環境構築等を進めることができます。

## 🛠 開発者向けリソース

> [!IMPORTANT]
> これ以降のセクションは、主に開発者等のコントリビューターを想定して記述しています。

### 📦 パッケージ管理

#### パッケージの追加

```sh
# 本番環境用のパッケージ追加
$ uv add {package_name}
# 開発環境用のパッケージ追加
$ uv add --dev {package_name}
```

#### パッケージの削除

```sh
# 本番環境用のパッケージ削除
$ uv remove {package_name}
# 開発環境用のパッケージ削除
$ uv remove --dev {package_name}
```

### 🔎 テスト

詳細は `test` ディレクトリ内の[`README`](../../tests/README.md)を参照してください。

### ✅ 静的コード解析

> [!NOTE]
> 静的コード解析は、[CI ワークフロー](../../.github/workflows/check.yml)上でも実行されます。

#### リンター

```sh
# リンターの適用（修正なし）
$ uv run ruff check {dir_name}
# リンターの適用
$ uv run ruff check {dir_name} --fix
```

#### フォーマッター

```sh
# フォーマッターの適用（修正なし）
$ uv run ruff format {dir_name} --check
# フォーマッターの適用
$ uv run ruff format {dir_name}
```

#### 型チェック

```sh
# mypyの実行
$ uv run mypy {dir_name}
```

#### プレコミットスクリプト

プレコミットスクリプトは [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) で設定されており、git 経由でコミットする毎に実行されます。実際にコミットせずに単体で挙動を確認したい場合は、以下のコマンドを実行してみましょう。

```sh
# 実際のコミットを行わずにプレコミットスクリプトを実行
$ uv run pre-commit run --all-files
```

### 📝 コメント・ドックストリング

コード内のドックストリングは [Google スタイル](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)に沿って書く必要があります。

### 📚 開発者向けドキュメント

ソースコードから自動生成された開発者向けドキュメントは[ここ](../../docs/core/)からアクセスできます。
