import scrapy

from crawler.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"  # スパイダーの識別名。コマンドラインから実行するときに使用
    allowed_domains = [
        "quotes.toscrape.com"
    ]  # クロールを許可するドメインのリスト。セキュリティ対策として重要
    start_urls = ["https://quotes.toscrape.com"]  # スクレイピングを開始するURLのリスト

    def parse(self, response):  # レスポンスを処理する主要なメソッド
        # ロガーを使用
        self.logger.info("Processing URL: %s", response.url)

        # ページ内のすべての引用を抽出
        for quote in response.css(
            "div.quote"
        ):  # CSSセレクタを使ってHTMLからデータを抽出
            item = QuoteItem()
            item["text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("small.author::text").get()
            item["tags"] = quote.css("a.tag::text").getall()

            # author_url = quote.css('a[href*="/author/"]::attr(href)').get()
            # if author_url:
            #     # 相対URLを絶対URLに変換
            #     author_url = response.urljoin(author_url)
            #     item['author_url'] = author_url

            #     # 著者ページもスクレイピング
            #     yield scrapy.Request(
            #         url=author_url,
            #         callback=self.parse_author,
            #         meta={'item': item}  # 名言の情報を次のコールバックに渡す
            #     )

            yield item

        # 次のページがあればparse()を実行
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
            # @see: https://doc-ja-scrapy.readthedocs.io/ja/latest/intro/tutorial.html#a-shortcut-for-creating-requests

    # def parse_author(self, response):
    #     # 前のコールバックから受け取った名言の情報
    #     item = response.meta.get("item")

    #     # 著者情報を抽出
    #     author_item = AuthorItem()
    #     author_item["name"] = response.css("h3.author-title::text").get()
    #     author_item["born_date"] = response.css("span.author-born-date::text").get()
    #     author_item["born_location"] = response.css(
    #         "span.author-born-location::text"
    #     ).get()
    #     author_item["bio"] = response.css("div.author-description::text").get().strip()
    #     author_item["url"] = response.url

    #     # 著者アイテムをyield
    #     yield author_item
