import { Env, Test, TestCase } from '../../types'
import { NextApiRequest, NextApiResponse } from 'next'
import {
  rankClient,
  RankEvalResponse,
  RankEvalRequestRequest,
} from '../../services/elasticsearch'
import {
  SearchTemplate,
  getSearchTemplates,
} from '../../services/search-templates'
import tests from '../../data/tests'
import { Pass } from '../../data/tests/pass'

function casesToRankEvalRequest(
  cases: TestCase[],
  template: SearchTemplate
): RankEvalRequestRequest<{ query: string }>[] {
  return cases.map((example: TestCase) => {
    return {
      id: example.query,
      template_id: template.id,
      params: {
        query: example.query,
      },
      ratings: example.ratings.map((id) => {
        return {
          _id: id,
          _index: template.index,
          rating: 3,
        }
      }),
    }
  })
}

export function rankEvalRequest(
  template: SearchTemplate,
  test: Test
): Promise<RankEvalResponse> {
  const { id, index } = template
  const { cases, metric, searchTemplateAugmentation } = test
  const requests = casesToRankEvalRequest(cases, template)
  const searchTemplate = searchTemplateAugmentation
    ? searchTemplateAugmentation(test, template.source)
    : template.source

  const body = {
    requests,
    metric,
    templates: [{ id, template: { source: searchTemplate } }],
  }

  const req = rankClient
    .rankEval<RankEvalResponse>({ index, body })
    .then((res) => res.body)

  return req
}

type TestResult = {
  label: string
  description: string
  pass: boolean
  results: {
    query: string
    result: Pass
  }[]
}

function runTests(tests: Test[], template: SearchTemplate) {
  const testResults: Promise<TestResult>[] = tests.map((test) =>
    rankEvalRequest(template, test)
      .then((res) => ({ res, test }))
      .then(({ res, test }) => {
        const results = Object.entries(res.details).map(([query, detail]) => ({
          query,
          result: test.pass(detail),
        }))
        return {
          label: test.label,
          description: test.description,
          pass: results.every((result) => result.result.pass),
          results,
        }
      })
  )

  return testResults
}

export default async (
  req: NextApiRequest,
  res: NextApiResponse
): Promise<void> => {
  const env = req.query.env ? req.query.env : 'prod'
  const searchTemplates = await getSearchTemplates(env as Env)

  // We run multiple tests with different metrics against different indexes
  // see: https://github.com/elastic/elasticsearch/issues/51680
  const responses = await Promise.all(
    searchTemplates
      .map((template) => runTests(tests[template.namespace], template))
      .reduce((cur, acc) => cur.concat(acc), [])
  )

  res.statusCode = 200
  res.setHeader('Content-Type', 'application/json')
  res.end(JSON.stringify(responses))
}
