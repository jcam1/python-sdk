# コードサンプル・実装例

このディレクトリでは、JPYC Python SDK を用いて JPYC コントラクトとやりとりを行うコードサンプルを複数用意しています。

## 🏃🏻 コードサンプルの実行

> [!IMPORTANT]
> コードサンプルの実行前に、ローカル環境でブロックチーンネットワーク（i.e., 実行クライアント）を立ち上げておく必要があります。[Foundry](https://book.getfoundry.sh/) や [Hardhat](https://hardhat.org/) のようなフレームワークや、[Geth](https://geth.ethereum.org/docs) のような実行クライアントを使用することでローカルネットワークを立ち上げることができます。

```sh
# `core`パッケージディレクトリに移動
$ cd python-sdk/packages/core
# `transfer.py`を実行
$ uv run examples/transfer.py
```

## 🌲 ディレクトリ構造

コマンド経由で、以下のコードサンプル（モジュール）を実行することができます。

|                                                            Module | Description                                                |
| ----------------------------------------------------------------: | :--------------------------------------------------------- |
|                                               [`main`](./main.py) | SDK クライアントの設定例                  |
|                                       [`transfer`](./transfer.py) | `transfer` メソッドを呼び出す実装例                  |
|                             [`transfer_from`](./transfer_from.py) | `approve` と `transferFrom` メソッドを呼び出す実装例 |
| [`transfer_with_authorization`](./transfer_with_authorization.py) |　`transferWithAuthorization` メソッドを呼び出す実装例 |
|   [`receive_with_authorization`](./receive_with_authorization.py) | `receiveWithAuthorization` メソッドを呼び出す実装例 |
|               [`cancel_authorization`](./cancel_authorization.py) | `cancelAuthorization` メソッドを呼び出す実装例       |
|                                           [`permit`](./permit.py) | `permit` メソッドを呼び出す実装例                    |
|                                               [`mint`](./mint.py) | `mint` メソッドを呼び出す実装例                      |
|                                     [`constants`](./constants.py) | コードサンプルで使用している定数群                          |
|                                             [`utils`](./utils.py) | コードサンプルで使用しているユーティリティ関数群                  |
