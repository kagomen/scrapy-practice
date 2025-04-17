## 環境構築

```bash
asdf plugin add python
asdf plugin add poetry

asdf install python 3.13.2
asdf install poetry 2.1.1

asdf set python 3.13.2
asdf set poetry 2.1.1

# 仮想環境を有効にする
poetry env activate
```

## Scrapy プロジェクトの作成

```
scrapy startproject crawler
```

以下のディレクトリが作成される

```
crawler/
├── scrapy.cfg            # プロジェクトの設定ファイル
└── crawler/              # プロジェクトのPythonモジュール
    ├── __init__.py
    ├── items.py          # データ項目の定義
    ├── middlewares.py    # ミドルウェアの定義
    ├── pipelines.py      # パイプラインの定義
    ├── settings.py       # プロジェクト設定
    └── spiders/          # スパイダーを置くディレクトリ
        └── __init__.py
```

## スパイダーの作成と基本構造

スパイダー：任意の Web サイトからデータを抽出するためのクラス

```bash
cd crawler

# ファイル名とスクレイピング対象のサイトを指定し実行
scrapy genspider quotes quotes.toscrape.com
# crawler/spiders/にquotes.pyが作成される
```

```py
# 作成されたquotes.pyの内容

import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'quotes'  # スパイダーの識別名
    allowed_domains = ["quotes.toscrape.com"]     # スクレイピングを許可するドメイン。これを指定しなければ、色んなURLを無限に辿り続ける可能性がある
    start_urls = ["https://quotes.toscrape.com"]  # スクレイピングを開始するURL

    def parse(self, response):
        # ここに抽出ロジックを書く
        pass
```

以下のように、spiders/に複数のスパイダーファイルを作成できる
これらは crawler/settings.py の設定が反映される
ファイル内で個別に設定を行うことも可能

```bash
crawler/
└── spiders/
    ├── __init__.py
    ├── quotes.py   # 名言サイト用スパイダー
    ├── books.py    # 書籍サイト用スパイダー
    └── news.py     # ニュースサイト用スパイダー
```

## CSS セレクタの基本

Scrapy では、HTML からデータを抽出するために CSS セレクタを使用する。

```py
def parse(self, response):
    # ページタイトルを取得
    title = response.css('title::text').get()

    # すべてのh2タグのテキストを取得
    headings = response.css('h2::text').getall()

    # 特定のクラスを持つ要素から情報を取得
    info = response.css('.info-class::text').get()

    # 複数要素から情報を取得
    for item in response.css('.item'):
        name = item.css('h3::text').get()
        price = item.css('.price::text').get()
        yield {
            'name': name,
            'price': price
        }
```

## スパイダーの実行

```bash
# scrapy.cfgが存在するディレクトリで実行する
# quotesはname属性に指定した値
scrapy crawl quotes
```

### 出力の指定

```bash
# JSONファイルとして保存
scrapy crawl quotes -O quotes.json

# CSVファイルとして保存
scrapy crawl quotes -O quotes.csv

# JSONLファイルとして保存
scrapy crawl quotes -O quotes.jsonl
# 途中で処理が終了された場合、JSONファイルだと最後の ] が書き込まれない可能性がある
# この状態のJSONファイルは「不完全」で、標準のJSONパーサーで読み込もうとするとエラーになる
# その点、JSONLファイルは1行ずつ{}で区切られるので大規模データをクロールするのに適している

# 上書き保存: -O
# 追加保存: -o
```

### ログの指定

```bash
# 重要なメッセージのみ表示
scrapy crawl quotes --loglevel=WARNING

# 詳細なログを表示
scrapy crawl quotes --loglevel=DEBUG

# ログファイルを出力
scrapy crawl quotes --logfile=quotes_spider.log
```

## Scrapy Shell

対話的にデータ抽出を試すためのツール

```bash
# URLを指定してシェルを起動
scrapy shell "https://quotes.toscrape.com"
# シェルが起動すると以下のオブジェクトを使って要素を抽出できる

# response: HTTPレスポンスオブジェクト
# request: HTTPリクエストオブジェクト
# spider: 仮想的なスパイダーインスタンス

# タイトルを取得
response.css('title::text').get()

# 最初の引用を取得
response.css('div.quote')[0].css('span.text::text').get()

# すべての著者名をリスト化
response.css('small.author::text').getall()

# XPathも使用可能
response.xpath('//span[@class="text"]/text()').get()
```

## スパイダーの詳細設定

```py
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    # クローリング速度の制限 (2秒間隔)
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    # User-Agentの設定
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

    def parse(self, response):
        # ...
```
