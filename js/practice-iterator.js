function genIterator(max = 10) {
  let i = 0
  return {
    next: () => {
      if (i >= max) {
        return {
          done: true,
        }
      }
      return {
        done: false,
        value: i++,
      }
    },
  }
}

const it = genIterator(10)
let a = it.next()
while (!a.done) {
  console.log(a.value)
  a = it.next()
}

const obj = {
  [Symbol.iterator]: genIterator(null, 100),
}

for (const i of obj) {
  console.log(i)
}
