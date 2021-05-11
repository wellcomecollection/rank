import { Env, Example, Rating } from '../../types'
import { NextApiRequest, NextApiResponse } from 'next'
import {
  RankEvalResponse,
  rankClient,
  RankEvalResponsWithMeta,
  RankDetail,
} from '../../services/elasticsearch'
import { Template, getSearchTemplates } from '../../services/search-templates'
import { indexToQueryType } from '../index'
import imageRatings from '../../data/ratings/images'
import workRatings from '../../data/ratings/works'

function formatExamples(examples: Example[], template: Template) {
  return examples.map((example: Example) => {
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

export function rankEvalRequests(
  template: Template
): Promise<RankEvalResponse>[] {
  const queryType = indexToQueryType(template.index)
  const ratings = { works: workRatings, images: imageRatings }[queryType]
  const requests = Object.entries(
    ratings
  ).map(([name, rating]: [string, Rating]) =>
    rankEvalRequest(template, name, rating)
  )
  return requests
}

export async function rankEvalRequest(
  template: Template,
  name: string,
  rating: Rating
): Promise<RankEvalResponsWithMeta> {
  const { id, index } = template
  const { examples, metric, searchTemplateAugmentation, pass } = rating
  const requests = formatExamples(examples, template)
  const searchTemplate = searchTemplateAugmentation
    ? searchTemplateAugmentation(rating, template.template)
    : template.template

  const body = {
    requests,
    metric,
    templates: [{ id, template: searchTemplate }],
  }

  const response = await rankClient
    .rankEval<RankEvalResponse>({ index, body })
    .then((resp) => {
      return {
        ...resp.body,
        index,
        pass: {
          pass: Object.entries(resp.body.details).every(
            ([, detail]: [string, RankDetail]) => {
              return pass(detail)
            }
          ),
          score: resp.body.metric_score,
        },
        queryId: `${indexToQueryType(index)}-${name}`,
        query: {
          method: 'POST',
          path: `${index}/_rank_eval`,
          body: JSON.stringify(resp.body),
        },
      }
    })

  return response
}

export default async (
  req: NextApiRequest,
  res: NextApiResponse
): Promise<void> => {
  const env = req.query.env ? req.query.env : 'prod'
  const searchTemplates = await getSearchTemplates(env as Env)

  // we allow for multiple requests to be made, because we're testing multiple
  // metrics against multiple indexes
  // see: https://github.com/elastic/elasticsearch/issues/51680
  const requests = searchTemplates.templates
    .map((template) => rankEvalRequests(template))
    .reduce((cur, acc) => cur.concat(acc), [])

  const responses = await Promise.all(requests)

  const response = {
    pass: responses.every((resp) => resp.metric_score === 1),
    rankings: responses,
  }

  res.statusCode = 200
  res.setHeader('Content-Type', 'application/json')
  res.end(JSON.stringify(response))
}
