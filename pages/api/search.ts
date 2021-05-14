import { NextApiRequest, NextApiResponse } from 'next'
import { Template, getSearchTemplates } from '../../services/search-templates'
import {
  rankClient,
  RankEvalResponsWithMeta,
  SearchResponse,
} from '../../services/elasticsearch'
import { rankEvalRequests } from './eval'
import { Endpoint } from '../search'

async function getCurrentQuery(endpoint: Endpoint): Promise<Template> {
  const searchTemplates = await getSearchTemplates('prod')
  const template = searchTemplates.templates.find((template) =>
    template.index.startsWith(`ccr--${endpoint}`)
  )
  return template
}

async function getTestQuery(endpoint: Endpoint): Promise<Template> {
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

export type ApiResponse = SearchResponse & {
  rankEval: RankEvalResponsWithMeta[]
}

export type ApiRequest = {
  query?: string
  useTestQuery?: 'true' | 'false'
  endpoint?: Endpoint
}

type Q = NextApiRequest['query']
const decoder = (q: Q) => ({
  query: q.query ? q.query.toString() : undefined,
  endpoint:
    q.endpoint === 'works' || q.endpoint === 'images'
      ? (q.endpoint as Endpoint)
      : ('works' as Endpoint),
  useTestQuery: q.useTestQuery === 'true' ?? false,
})

export default async (
  req: NextApiRequest,
  res: NextApiResponse
): Promise<void> => {
  const { endpoint, query, useTestQuery } = decoder(req.query)

  const template = useTestQuery
    ? await getTestQuery(endpoint)
    : await getCurrentQuery(endpoint)

  const rankEvalReqs = rankEvalRequests(template)
  const searchReq = rankClient
    .searchTemplate<SearchResponse>({
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
    .then((res) => res.body)

  const requests: [
    Promise<SearchResponse>,
    Promise<RankEvalResponsWithMeta[]>
  ] = [searchReq, Promise.all(rankEvalReqs)]

  const [searchResp, ...[rankEvalResps]] = await Promise.all(requests)
  const response: ApiResponse = {
    ...searchResp,
    rankEval: rankEvalResps,
  }

  res.statusCode = 200
  res.setHeader('Content-Type', 'application/json')
  res.end(JSON.stringify(response))
}
