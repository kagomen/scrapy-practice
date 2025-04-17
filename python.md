# Python 基礎

## `def`

```py
# 関数定義
def say_hello(name):
    return f"Hello, {name}!"

# cf: JS
# function sayHello(name) {
#     return `Hello, ${name}!`
# }
```

## `for`

```py
# リストの各要素をループ
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# cf: JS
# const fruits = ["apple", "banana", "cherry"]
# for (const fruit of fruits) {
#     console.log(fruit)
# }
```

## `yield` - 値を返し、関数の状態を保持するジェネレータを作成

```py
# ジェネレータ関数
def count_to_three():
    yield 1
    yield 2
    yield 3

# 使用例
for num in count_to_three():
    print(num)  # 1, 2, 3と出力される

# cf: JS
# function* countToThree() {
#     yield 1
#     yield 2
#     yield 3
# }
#
# for (const num of countToThree()) {
#     console.log(num)
# }
```

Scrapy では、yield を使って抽出したアイテムを返す。
このため、大量のデータをメモリに一度に保持することなく処理可能。

### ジェネレータの特性:

- yield を使うと、Python はジェネレータ関数を作成する
- ジェネレータは「遅延評価（lazy evaluation）」と呼ばれる方式で動作する

### メモリ使用量の違い:

- return の場合: すべてのアイテムを一度にメモリに保持する必要がある。→ 大量データの場合、メモリ不足に
- yield の場合: 一度に 1 項目だけをメモリに保持し、処理が終わったら次の項目を生成する

```py
# returnを使った場合
def get_all_items():
    items = []
    for i in range(1000000):  # 100万項目のデータ
        items.append({"id": i})
    return items  # 100万項目をすべてメモリに保持してから返す

# yieldを使った場合
def get_items_generator():
    for i in range(1000000):  # 100万項目のデータ
        yield {"id": i}  # 1項目ずつ生成して返す
```

### 処理失敗時の挙動

yield を使った場合の失敗処理は、Scrapy の設定や使っているデータストレージの仕組みに依存する。

基本的な挙動:
yield されたアイテムは順次処理されるため、エラーが発生する前に処理されたアイテムはすでに保存される。
つまり、途中で失敗しても、それまでに処理されたデータは残る。

トランザクション的な挙動が必要な場合:
Scrapy のパイプラインで明示的にトランザクション処理を実装する必要がある。
例えば、データベースに保存する場合は、スクレイピング開始時にトランザクションを開始し、すべて成功したらコミット、失敗したらロールバックするよう実装可能。
しかし大規模なスクレイピングでは、完全なトランザクションよりも「バッチ処理」が一般的。例えば、100 アイテムごとにコミットするなど、部分的に成功を確定させる方法を取ることが多い。

5 行の yield があり、3 行目の yield で処理が失敗した場合、4,5 行目の yield は実行されない。
Scrapy の場合、スパイダー内でエラーが発生すると：

- リクエストは中断される
- エラーはログに記録される
- Scrapy は他のリクエストの処理を実行する（設定によっては失敗したリクエストを再試行することも可能）

リクエストはどこで区切られるか？→`parse()`が呼び出される単位

### 補足

- 遅延評価：結果が必要になるまで計算を遅らせる評価戦略
- ストリーム処理：データ全体が利用可能になる前に、データの一部を順次処理していく手法
- ジェネレータ：メモリ効率を向上させるための仕組み（データを一度にすべて生成せず、必要に応じて生成）
- 非同期処理：CPU 効率を向上させるための仕組み（I/O 待ち時間中に他の処理を実行可能に）

ジェネレータも async/await も、それぞれの方法でストリーム処理を実現するために使うことができる

- ジェネレータ：メモリ効率の良いストリーム処理
- async/await：I/O 効率の良いストリーム処理

理想的には両方を組み合わせると効率的。
