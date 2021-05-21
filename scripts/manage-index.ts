import {
  createTestIndex,
  deleteTestIndex,
  getCloudIndicies,
  getLocalIndicies,
  updateTestIndex,
} from '../services/index-management'

import inquirer from 'inquirer'

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
    const indexNames = await getLocalIndicies()
    console.log('creating index')
    console.log(indexNames)
  } else if (action === 'Update an existing index') {
    const indexNames = await getCloudIndicies()
    console.log('updating index')
    console.log(indexNames)
  } else if (action === 'Delete an existing index') {
    const indexNames = await getCloudIndicies()
    console.log('deleting index')
    console.log(indexNames)
  }
}

main()
