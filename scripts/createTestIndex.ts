import { rankClient } from '../services/elasticsearch'

async function go() {
  const [namespace, indexName] = process.argv.slice(2)
  if (!namespace || !indexName) {
    throw new Error(
      'Please specifiy a `namespace` and `indexName` e.g. yarn createTestIndex works works-100'
    )
  }

  const indexConfig = await import(`../data/indices/${namespace}`).then(
    (mod) => mod.default
  )
  const { body: putIndexRes } = await rankClient.indices
    .create({
      index: indexName,
      body: indexConfig,
    })
    .catch((err) => {
      console.error(err.meta.body)
      return err
    })
  console.info(putIndexRes)
}

go()
