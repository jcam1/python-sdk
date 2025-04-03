使用方法
======

基本的な使い方
-----------

.. code-block:: python

   from jpyc_sdk import SdkClient, JPYC
   import os
   from dotenv import load_dotenv

   # 環境変数をロード
   load_dotenv()

   # SdkClientインスタンスを初期化
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

   # トークンの総供給量を取得
   async def get_total_supply():
       total_supply = await jpyc.total_supply()
       print(f"Total Supply: {total_supply}")

環境変数
-------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - 環境変数
     - 説明
   * - ``SDK_ENV``
     - SDKの環境（``local``など）
   * - ``CHAIN_NAME``
     - チェーン名（``ethereum``, ``polygon``など）
   * - ``NETWORK_NAME``
     - ネットワーク名（``mainnet``, ``sepolia``など）
   * - ``RPC_ENDPOINT``
     - RPC接続先URL
   * - ``PRIVATE_KEY``
     - アカウントの秘密鍵 