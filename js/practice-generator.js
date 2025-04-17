function* genIterator() {
  yield 1
  yield 2
  return 3
}

const it = genIterator()
console.log(it.next())
console.log(it.next())
console.log(it.next())
console.log(it.next())
console.log(it.next())

// (2) {value: 1, done: false}
// (2) {value: 2, done: false}
// (2) {value: 3, done: true}
// (2) {value: undefined, done: true}
// (2) {value: undefined, done: true}

function* genIterator2(max = 3) {
  let i = 0
  while (i < max) {
    yield i++
  }
  return
}

const it2 = genIterator2()

console.log(it2.next())
console.log(it2.next())
console.log(it2.next())
console.log(it2.next())
console.log(it2.next())

// (2) {value: 1, done: false}
// (2) {value: 2, done: false}
// (2) {value: 3, done: true}
// (2) {value: undefined, done: true}
// (2) {value: undefined, done: true}

let a = it2.next()
while (!a.done) {
  console.log(a.value)
  a = it2.next()
}

// 0
// 1
// 2

const obj = {
  [Symbol.iterator]: genIterator2,
}
for (const i of obj) {
  console.log(i)
}

// generatorの場合は反復可能オブジェクトを作成しなくてもそのままforループに使用できる
for (const i of genIterator2()) {
  console.log(i)
}
