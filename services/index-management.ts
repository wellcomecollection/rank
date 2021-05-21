import { rankClient } from './elasticsearch'

export async function getLocalIndicies() {
  return []
}

export async function getCloudIndicies() {
  const response = await rankClient.cat.indices({ format: 'json' })
  return response.body
    .map((index) => index.index)
    .filter((index) => !index.startsWith('.'))
}

async function getIndexConfig(indexName: string) {
  const indexConfig = await import(`../data/indices/${indexName}`).then(
    (mod) => mod.default
  )
  return indexConfig
}

export async function createTestIndex(indexName) {
  const indexConfig = await getIndexConfig(indexName)
  const { body: putIndexRes } = await rankClient.indices
    .create({
      index: indexName,
      body: {
        ...indexConfig,
        settings: {
          ...indexConfig.settings,
          index: {
            ...indexConfig.settings.index,
            number_of_shards: 1,
            number_of_replicas: 0,
          },
        },
      },
    })
    .catch((err) => {
      console.error(err.meta.body)
      return err
    })
  console.info(putIndexRes)
}

export async function updateTestIndex(indexName) {
  const indexConfig = await getIndexConfig(indexName)
  const { body: closeIndedxRes } = await rankClient.indices.close({
    index: indexName,
  })
  console.info(closeIndedxRes)

  const { body: putSettingsRes } = await rankClient.indices
    .putSettings({
      index: indexName,
      body: {
        ...indexConfig.settings,
      },
    })
    .catch((err) => {
      console.error(err.meta.body)
      return err
    })
  console.info(putSettingsRes)

  const { body: putMappingRes } = await rankClient.indices
    .putMapping({
      index: indexName,
      body: {
        ...indexConfig.mappings,
      },
    })
    .catch((err) => {
      console.error(err.meta.body)
      return err
    })

  console.info(putMappingRes)

  const { body: openIndedxRes } = await rankClient.indices.open({
    index: indexName,
  })
  console.info(openIndedxRes)
}

export async function deleteTestIndex(indexName) {
  const { body: deleteIndexRes } = await rankClient.indices
    .delete({
      index: indexName,
    })
    .catch((err) => {
      console.error(err.meta.body)
      return err
    })
  console.info(deleteIndexRes)
}
