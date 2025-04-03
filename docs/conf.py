import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# プロジェクト情報
project = 'JPYC Python SDK'
copyright = '2024, JPYC Inc.'
author = 'JPYC Inc.'
version = '0.1.0'

# 拡張機能
extensions = [
    'sphinx.ext.autodoc',  # 自動ドキュメント生成
    'sphinx.ext.viewcode',  # ソースコードへのリンク
    'sphinx.ext.napoleon',  # Google/Numpyスタイルdocstringsのサポート
    'sphinx.ext.autosummary',  # 自動サマリー生成
    'sphinx.ext.githubpages',  # GitHub Pagesのサポート
    # 'myst_parser',  # Markdownサポート - 必要ない場合はコメントアウト
]

# テーマ設定
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# 自動APIドキュメント生成の設定
autosummary_generate = True  # autosummaryを使用して自動生成
autodoc_typehints = 'description'
autodoc_member_order = 'bysource'
autoclass_content = 'both'

# 出力オプション
html_show_sourcelink = True
html_show_sphinx = False

# 言語設定
language = 'ja'

# ソースコードへのリンク
html_context = {
    "display_github": True,
    "github_user": "jcam1",
    "github_repo": "python-sdk", 
    "github_version": "main",
    "conf_py_path": "/docs/",
} 