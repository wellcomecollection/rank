import { NextApiRequest, NextApiResponse } from 'next'
import { SearchResponse, rankClient } from '../../services/elasticsearch'
import {
  SearchTemplate,
  getSearchTemplates,
} from '../../services/search-templates'
import { TestResult, runTests } from './eval'
import { Namespace } from '../search'
import tests from '../../data/tests'

async function getCurrentQuery(namespace: Namespace): Promise<SearchTemplate> {
  const searchTemplates = await getSearchTemplates('prod')
  const template = searchTemplates.find((template) =>
    template.index.startsWith(`ccr--${namespace}`)
  )
  return template
}

async function getTestQuery(namespace: Namespace): Promise<SearchTemplate> {
  const currentTemplate = await getCurrentQuery(namespace)
  const query = await import(`../../data/queries/${namespace}`).then(
    (q) => q.default
  )

  return {
    id: 'test',
    index: currentTemplate.index,
    namespace: namespace,
    source: { query: query },
  }
}

export type ApiResponse = SearchResponse & {
  results: TestResult[]
}

export type ApiRequest = {
  query?: string
  useTestQuery?: 'true' | 'false'
  namespace?: Namespace
}

type Q = NextApiRequest['query']
const decoder = (q: Q) => ({
  query: q.query ? q.query.toString() : undefined,
  namespace:
    q.namspace === 'works' || q.namspace === 'images'
      ? (q.namspace as Namespace)
      : ('works' as Namespace),
  useTestQuery: q.useTestQuery === 'true' ?? false,
})

export default async (
  req: NextApiRequest,
  res: NextApiResponse
): Promise<void> => {
  const { namespace, query, useTestQuery } = decoder(req.query)

  const template = useTestQuery
    ? await getTestQuery(namespace)
    : await getCurrentQuery(namespace)

  const resultsReq = runTests(tests[template.namespace], template)
  const searchReq = rankClient
    .searchTemplate<SearchResponse>({
      index: template.index,
      body: {
        explain: true,
        source: {
          ...template.source,
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

  const requests: [Promise<SearchResponse>, Promise<TestResult[]>] = [
    searchReq,
    Promise.all(resultsReq),
  ]

  const [searchResp, ...[results]] = await Promise.all(requests)
  const response: ApiResponse = {
    ...searchResp,
    results,
  }

  res.statusCode = 200
  res.setHeader('Content-Type', 'application/json')
  res.end(JSON.stringify(response))
}
