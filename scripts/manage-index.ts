import {
  createTestIndex,
  deleteTestIndex,
  getClusterIndicies,
  getLocalIndicies,
  updateTestIndex,
} from '../services/index-management'

import inquirer from 'inquirer'
import { type } from 'node:os'

async function main() {
  const { action } = await inquirer.prompt([
    {
      type: 'list',
      name: 'action',
      message: 'What do you want to do?',
      choices: [
        'Create a new index',
        'Update an existing index',
        'Delete an existing index',
      ],
    },
  ])

  if (action === 'Create a new index') {
    const local = await getLocalIndicies()
    const cluster = await getClusterIndicies()
    // should only be able to create indices which don't exist
    const indexNames = local.filter((n) => !cluster.includes(n))
    const { indexName } = await inquirer.prompt([
      {
        type: 'list',
        name: 'indexName',
        message: 'Which index would you like to create?',
        choices: indexNames,
      },
    ])
    createTestIndex(indexName)
  } else if (action === 'Update an existing index') {
    const local = await getLocalIndicies()
    const cluster = await getClusterIndicies()
    // should only be able to update indexes which exist locally AND in cluster
    const indexNames = local.filter((n) => cluster.includes(n))
    const { indexName } = await inquirer.prompt([
      {
        type: 'list',
        name: 'indexName',
        message: 'Which index would you like to update?',
        choices: indexNames,
      },
    ])
    updateTestIndex(indexName)
  } else if (action === 'Delete an existing index') {
    const indexNames = await getClusterIndicies()
    const { indexName } = await inquirer.prompt([
      {
        type: 'list',
        name: 'indexName',
        message: 'Which index would you like to delete?',
        choices: indexNames,
      },
    ])
    const { confirmed } = inquirer.prompt([
      {
        type: 'confirm',
        name: 'confirmed',
        message: 'Are you sure?',
        default: false,
      },
    ])
    if (confirmed) {
      deleteTestIndex(indexName)
    }
  }
}

main()
