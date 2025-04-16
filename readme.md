```
asdf plugin add python
asdf plugin add poetry

asdf install python 3.13.2
asdf install poetry 2.1.1

asdf set python 3.13.2
asdf set poetry 2.1.1

poetry env activate
```

```
scrapy startproject crawler

crawler/
├── scrapy.cfg            # プロジェクトの設定ファイル
└── crawler/       # プロジェクトのPythonモジュール
    ├── __init__.py
    ├── items.py          # データ項目の定義
    ├── middlewares.py    # ミドルウェアの定義
    ├── pipelines.py      # パイプラインの定義
    ├── settings.py       # プロジェクト設定
    └── spiders/          # スパイダーを置くディレクトリ
        └── __init__.py
```

```
cd crawler

ファイル名とスクレイピング対象のサイトを指定し、crawler配下にスパイダーを作成
scrapy genspider quotes quotes.toscrape.com



```
