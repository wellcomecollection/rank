import { Env, Example } from '../../types'
import { NextApiRequest, NextApiResponse } from 'next'
import { RankEvalResponse, rankClient } from '../../services/elasticsearch'
import { Template, getSearchTemplates } from '../../services/search-templates'

import imageRatings from '../../data/ratings/images'
import { indexToQueryType } from '../index'
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
  const requests = Object.entries(ratings).map(([name, { examples, metric }]) =>
    rankEvalRequest(template, name, examples, metric)
  )
  return requests
}

export async function rankEvalRequest(
  template: Template,
  name: string,
  examples: Example[],
  metric
): Promise<RankEvalResponse> {
  const { id, index } = template
  const requests = formatExamples(examples, template)
  const body = {
    requests,
    metric,
    templates: [{ id, template: template.template }],
  }

  if (name === 'negative') {
    // To avoid running exceptionally long recall queries for our negative
    // examples, we intercept the template and add a filter to only include
    // results from the set of target IDs. This should have no effect on the
    // final result, as explained in the comment below.
    const targetIds = examples.flatMap((x) => x.ratings)
    const augmentedTemplate = {
      source: {
        query: {
          bool: {
            must: [body.templates[0].template.source.query],
            filter: { terms: { _id: targetIds } },
          },
        },
      },
    }
    body.templates[0].template = augmentedTemplate
  }

  const response = await rankClient
    .rankEval<RankEvalResponse>({ index, body })
    .then((resp) => {
      return {
        ...resp.body,
        index,
        queryId: `${indexToQueryType(index)}-${name}`,
        query: {
          method: 'POST',
          path: `${index}/_rank_eval`,
          body: JSON.stringify(resp.body),
        },
      }
    })

  if (name === 'negative') {
    // For our negative examples, we want to check that the target IDs _don't_
    // appear in the list of results. Rank_eval doesn't have a neat way of doing
    // this out of the box, but we know that the response's metric_score will be
    // 0 if and only if the ID isn't included in the results. If the ID is
    // included anywhere in the list, the score for the recall metric will be > 0.
    //
    // We therefore intercept the result here. If the score is 0, we manually
    // set it to 1 (ie pass). Otherwise, it's set to 0 (ie fail).
    console.log(JSON.stringify(response.details, null, 2))
    Object.values(response.details).forEach((search) => {
      if (search.metric_score === 0) {
        search.metric_score = 1
      } else {
        search.metric_score = 0
      }
    })
  }

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
