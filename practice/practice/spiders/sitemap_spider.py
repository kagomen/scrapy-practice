from datetime import datetime

from scrapy.spiders import SitemapSpider


class Spider(SitemapSpider):
    name = "sitemap_spider"
    allowed_domains = ["freeto.jp"]
    sitemap_urls = ["https://freeto.jp/sitemap.xml"]

    def sitemap_filter(self, entries):
        today = datetime.now().date()
        self.logger.debug(f"Today: {today}")

        for entry in entries:
            date_time = datetime.strptime(
                entry["lastmod"], "%Y-%m-%dT%H:%M:%S%z"
            ).date()
            self.logger.debug(f"date_time: {date_time}")
            if date_time == today:
                yield entry

    def parse(self, response):
        yield {"url": response.url}
