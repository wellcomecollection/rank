import { NextApiRequest, NextApiResponse } from 'next'
import { Template, getSearchTemplates } from '../../services/search-templates'
import { rankClient } from '../../services/elasticsearch'
import { rankEvalRequests } from './eval'

async function getCurrentQuery(endpoint: string): Promise<Template> {
  const searchTemplates = await getSearchTemplates('prod')
  const template = searchTemplates.templates.find((template) =>
    template.index.startsWith(`ccr--${endpoint}`)
  )
  return template
}

async function getTestQuery(endpoint: string): Promise<Template> {
  const currentTemplate = await getCurrentQuery(endpoint)
  const query = await import(`../../data/queries/${endpoint}`).then(
    (q) => q.default
  )

  return {
    id: 'test',
    index: currentTemplate.index,
    template: { source: { query: query } },
  }
}

export default async (
  req: NextApiRequest,
  res: NextApiResponse
): Promise<void> => {
  const { query, useTestQuery, endpoint } = req.query
  const template = useTestQuery
    ? await getTestQuery(endpoint as string)
    : await getCurrentQuery(endpoint as string)

  const rankEvalReqs = rankEvalRequests(template)
  const searchReq = rankClient.searchTemplate({
    index: template.index,
    body: {
      explain: true,
      source: {
        ...template.template.source,
        track_total_hits: true,
        highlight: {
          pre_tags: ['<em class="bg-yellow-200">'],
          post_tags: ['</em>'],
          fields: { '*': { number_of_fragments: 0 } },
        },
      },
      params: { query },
    },
  })

  const requests = [searchReq, ...rankEvalReqs]
  const [searchResp, ...rankEvalResps] = await Promise.all(requests as any[])

  res.statusCode = 200
  res.setHeader('Content-Type', 'application/json')
  res.end(
    JSON.stringify({
      ...searchResp.body,
      rankEval: rankEvalResps,
    })
  )
}
