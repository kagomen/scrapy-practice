# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    # 名言に関する情報
    text = scrapy.Field()  # 名言のテキスト
    author = scrapy.Field()  # 著者名
    # author_url = scrapy.Field()    # 著者詳細ページのURL
    tags = scrapy.Field()  # 名言に関連するタグ（リスト）
    author_first_name = scrapy.Field()  # 著者の名
    author_last_name = scrapy.Field()  # 著者の姓


# class AuthorItem(scrapy.Item):
#     # 著者に関する情報
#     name = scrapy.Field()          # 著者名
#     born_date = scrapy.Field()     # 生年月日
#     born_location = scrapy.Field() # 出生地
#     bio = scrapy.Field()           # 経歴
#     url = scrapy.Field()           # 著者ページのURL
