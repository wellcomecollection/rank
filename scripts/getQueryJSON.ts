import fs from 'fs'
;
(async function go() {
  const [queryName] = process.argv.slice(2)
  const query = await import(`../data/queries/${queryName}.ts`).then(
    (mod) => mod.default
  )

  fs.writeFile(
    `data/queries/${queryName}.json`,
    JSON.stringify(query, null, 2),
    function (err) {
      if (err) throw err
      console.log('Saved!')
    }
  )
})()
