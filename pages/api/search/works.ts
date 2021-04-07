import { NextApiRequest, NextApiResponse } from 'next'
import {
  Template,
  getSearchTemplates
} from '../../../services/search-templates'

import { client } from '../../../services/elasticsearch'
import { rankEvalRequests } from '../eval'

async function getCurrentQuery (): Promise<Template> {
  const searchTemplates = await getSearchTemplates('prod')
  const template = searchTemplates.templates.find((template) =>
    template.index.startsWith('works')
  )

  return template
}
async function getTestQuery (id: string): Promise<Template> {
  const currentTemplate = await getCurrentQuery()
  const index = currentTemplate.index
  const query = await import(`../../../queries/${id}`).then((q) => q.default)

  return {
    id,
    index,
    template: { source: { query: query } }
  }
}

export default async (req: NextApiRequest, res: NextApiResponse): Promise<void> => {
  const { query, queryId } = req.query

  const template = queryId
    ? await getTestQuery(queryId.toString())
    : await getCurrentQuery()

  const rankEvalReqs = rankEvalRequests(template)
  const searchQuery = query ? template : await getTestQuery('match-all')

  const searchReq = client.searchTemplate({
    index: template.index,
    body: {
      explain: true,
      source: {
        ...searchQuery.template.source,
        size: 1000,
        track_total_hits: true,
        highlight: {
          pre_tags: ['<em class="bg-yellow-200">'],
          post_tags: ['</em>'],
          fields: { '*': { number_of_fragments: 0 } }
        }
      },
      params: {
        query
      }
    }
  })

  const requests = [searchReq, ...rankEvalReqs]
  const [searchResp, ...rankEvalResps] = await Promise.all(requests as any[])

  res.statusCode = 200
  res.setHeader('Content-Type', 'application/json')
  res.end(
    JSON.stringify({
      ...searchResp.body,
      rankEval: rankEvalResps
    })
  )
}
