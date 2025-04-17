# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re  # python標準のregexライブラリ

from itemadapter import ItemAdapter


class TextCleaningPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("text"):
            # 引用符を削除
            text = adapter.get("text")
            text = re.sub(r"^“|”$", "", text)
            # 余分な空白を削除
            adapter["text"] = text.strip()
        return item


# re.sub(pattern, replacement, string, count=0, flags=0)

# pattern: 検索する正規表現パターン
# replacement: パターンにマッチした部分を置き換えるテキスト
# string: 検索と置換を行う対象である元の文字列
# count (省略可): 置換する最大回数（デフォルトは0で、すべて置換）
# flags (省略可): 正規表現のフラグ（例：大文字小文字を区別しない等）


class AuthorNamesPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("author"):
            # 著者名をフルネームと姓名に分割
            name_parts = adapter.get("author").split()
            if len(name_parts) >= 2:
                adapter["author_first_name"] = name_parts[0]
                adapter["author_last_name"] = " ".join(name_parts[1:])
        return item
