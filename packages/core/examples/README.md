# Examples

This directory contains a collection of code examples of using the SDK.

## 🏃🏻 Run Code Examples

Before running any examples, please make sure to start a blockchain network (i.e., execution client) on localhost. You can use some framework (e.g., [Foundry](https://book.getfoundry.sh/), [Hardhat](https://hardhat.org/)) or some direct client (e.g., [Geth](https://geth.ethereum.org/docs)).

```sh
# cd into one of the package directories (e.g., `core`)
$ cd python-sdk/packages/core
# run a python file (e.g., `transfer`)
$ uv run examples/transfer.py
```

## 🌲 Directory Structure

|                                                            Module | Description                                                |
| ----------------------------------------------------------------: | :--------------------------------------------------------- |
|                                               [`main`](./main.py) | Code example that configures SDK clients.                  |
|                                       [`transfer`](./transfer.py) | Code example that uses `transfer` method.                  |
|                             [`transfer_from`](./transfer_from.py) | Code example that uses `approve` & `transferFrom` methods. |
| [`transfer_with_authorization`](./transfer_with_authorization.py) | Code example that uses `transferWithAuthorization` method. |
|   [`receive_with_authorization`](./receive_with_authorization.py) | Code example that uses `receiveWithAuthorization` method.  |
|               [`cancel_authorization`](./cancel_authorization.py) | Code example that uses `cancelAuthorization` method.       |
|                                           [`permit`](./permit.py) | Code example that uses `permit` method.                    |
|                                               [`mint`](./mint.py) | Code example that uses `mint` method.                      |
|                                     [`constants`](./constants.py) | Some constants for code examples.                          |
|                                             [`utils`](./utils.py) | Some utility functions for code examples.                  |
