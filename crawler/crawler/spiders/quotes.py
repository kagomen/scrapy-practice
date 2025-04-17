import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"  # スパイダーの識別名。コマンドラインから実行するときに使用
    allowed_domains = ["quotes.toscrape.com"]  # クロールを許可するドメインのリスト。セキュリティ対策として重要
    start_urls = ["https://quotes.toscrape.com"]  # スクレイピングを開始するURLのリスト

    def parse(self, response):  # レスポンスを処理する主要なメソッド
        # ロガーを使用
        self.logger.info('Processing URL: %s', response.url)

        # 要素が見つかるか確認
        quotes = response.css('div.quote')
        self.logger.info('Found %d quotes', len(quotes))

        # ページ内のすべての引用を抽出
        for quote in response.css('div.quote'):  # CSSセレクタを使ってHTMLからデータを抽出
            yield {  # Python のジェネレータ構文で、データを一つずつ返す
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        
        # 次のページがあれば移動
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)