# XPath（XML Path Language）

- XML ドキュメント内の要素や属性を特定するための言語
- HTML も XML の一種として扱えるため、Web スクレイピングでも使用される
- XML ドキュメントの操作に特化している

## XPath の基本構文

- `//` - ドキュメント内のどこにでもある要素を選択
- `/` - 直接の子要素を選択
- `@` - 属性を選択
- `[]` - 条件を指定
- `text()` - テキストノードを選択
- `..` - 親要素を選択

```py
# XPathの使用例

def parse(self, response):
    # タイトルを取得
    title = response.xpath('//title/text()').get()

    # 特定のクラスを持つすべてのリンク
    links = response.xpath('//a[@class="product-link"]/@href').getall()

    # 条件に一致する要素を選択
    in_stock_products = response.xpath('//div[contains(@class, "product")][.//span[contains(text(), "在庫あり")]]')

    for product in in_stock_products:
        name = product.xpath('./h2/text()').get()
        price = product.xpath('./span[@class="price"]/text()').get()
        yield {
            'name': name,
            'price': price
        }
```

### コンテキストノード

XPath では、`.`は「現在のコンテキストノード」を表し、「今選択している要素を起点として」という意味になる。

```python
for product in response.xpath('//div[@class="product"]'):
    name = product.xpath('./h2/text()').get()
    price = product.xpath('./span[@class="price"]/text()').get()
```

1. まず `//div[@class="product"]` で「すべての product クラスを持つ div 要素」を選択
2. それらの要素に対して `for` ループを回す
3. 各 `product` 要素に対して、その中にある `h2` と `span` を取得する

→`./h2/text()` の `.` が「現在処理中の product 要素」を表している。

また、`//div[./span[@class="sold-out"]]`と`//div[span[@class="sold-out"]]`は同じ。

#### 他の使用例

```bash
# 「子要素に "sold-out" クラスの span を持つ div」を選択する
//div[./span[@class="sold-out"]]

# 「現在のノードの下にあるどこかの img 要素」を選択する（子孫要素すべてが対象）
.//img

# 「"product" クラスを持ち、かつ子要素の p に "在庫あり" というテキストがある div」を選択する
//div[@class="product" and ./p/text()="在庫あり"]
```
