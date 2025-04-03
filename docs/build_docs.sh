#!/bin/bash
# ドキュメント生成用のシェルスクリプト

# APIドキュメントを生成
echo "APIドキュメントを生成中..."
poetry run sphinx-apidoc -f -o docs/api jpyc_sdk

# HTMLドキュメントをビルド
echo "HTMLドキュメントをビルド中..."
poetry run sphinx-build -b html -a -E docs docs/_build/html

echo "ドキュメント生成完了！docs/_build/html ディレクトリを確認してください。" 