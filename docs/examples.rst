コード例
======

JPYC Python SDKを使用する基本的な例を以下に示します。

サンプルコード
===========

トークン残高の取得
--------------

.. code-block:: python

   import asyncio
   from jpyc_sdk import SdkClient, JPYC
   from dotenv import load_dotenv
   import os

   async def get_balance():
       # 環境変数をロード
       load_dotenv()
       
       # SDKクライアントの初期化
       sdk_client = SdkClient(
           chain_name=os.getenv("CHAIN_NAME"),
           network_name=os.getenv("NETWORK_NAME"),
           rpc_endpoint=os.getenv("RPC_ENDPOINT")
       )
       
       # アカウントとクライアントの作成
       account = sdk_client.create_private_key_account()
       client = sdk_client.create_local_client(account=account)
       
       # JPYCインスタンスの初期化
       jpyc = JPYC(client=client)
       
       # アドレスの残高を取得
       address = "0x..."  # 残高を確認したいアドレス
       balance = await jpyc.balance_of(address)
       
       print(f"Balance: {balance}")

   # 非同期関数を実行
   asyncio.run(get_balance())

トークンの送信
-----------

.. code-block:: python

   import asyncio
   from jpyc_sdk import SdkClient, JPYC
   from dotenv import load_dotenv
   import os

   async def transfer_tokens():
       # 環境変数をロード
       load_dotenv()
       
       # SDKクライアントの初期化
       sdk_client = SdkClient(
           chain_name=os.getenv("CHAIN_NAME"),
           network_name=os.getenv("NETWORK_NAME"),
           rpc_endpoint=os.getenv("RPC_ENDPOINT")
       )
       
       # アカウントとクライアントの作成
       account = sdk_client.create_private_key_account()
       client = sdk_client.create_local_client(account=account)
       
       # JPYCインスタンスの初期化
       jpyc = JPYC(client=client)
       
       # トークンを送信する宛先アドレスと金額
       recipient = "0x..."  # 送信先アドレス
       amount = 1000  # 送信金額（単位はJPYC）
       
       # 送信前の残高を確認
       sender_balance_before = await jpyc.balance_of(account.address)
       recipient_balance_before = await jpyc.balance_of(recipient)
       
       print(f"Sender balance before: {sender_balance_before}")
       print(f"Recipient balance before: {recipient_balance_before}")
       
       # トークンを送信
       tx_hash = await jpyc.transfer(recipient, amount)
       print(f"Transaction hash: {tx_hash}")
       
       # トランザクションの完了を待機（実際の実装ではブロック確認を待つ方が良い）
       await asyncio.sleep(15)
       
       # 送信後の残高を確認
       sender_balance_after = await jpyc.balance_of(account.address)
       recipient_balance_after = await jpyc.balance_of(recipient)
       
       print(f"Sender balance after: {sender_balance_after}")
       print(f"Recipient balance after: {recipient_balance_after}")

   # 非同期関数を実行
   asyncio.run(transfer_tokens())

より多くのサンプルについては、別のリポジトリにあるサンプルコードを参照してください。 