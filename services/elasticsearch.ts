/* eslint-disable camelcase */
import { Client } from '@elastic/elasticsearch'
import { Pass } from '../data/ratings/pass'

const {
  ES_RANK_USER,
  ES_RANK_PASSWORD,
  ES_RANK_CLOUD_ID,
  ES_RATINGS_USER,
  ES_RATINGS_PASSWORD,
  ES_RATINGS_CLOUD_ID,
} = process.env

type PrecisionMetricResponse = {
  precision: {
    relevant_docs_retrieved: number
    docs_retrieved: number
  }
}

type RecallMetricResponse = {
  recall: {
    relevant_docs_retrieved: number
    docs_retrieved: number
  }
}

type MetricResponse = PrecisionMetricResponse | RecallMetricResponse

export type RankDetail = {
  metric_score: number
  unrated_docs: unknown[]
  hits: unknown[]
  metric_details: MetricResponse
}

export type RankEvalResponse<DetailKeys extends string = string> = {
  metric_score: number
  details: Record<DetailKeys, RankDetail>
}

type PrecisionMetric = {
  precision: {
    relevant_rating_threshold: number
    k: number
  }
}

type RecallMetric = {
  recall: {
    relevant_rating_threshold: number
    k: number
  }
}

export type Metric = PrecisionMetric | RecallMetric

type RankEvalRequestRating<Rating = 0 | 1 | 2 | 3> = {
  _index: string
  _id: string
  rating: Rating
}

type RankEvalRequestRequest<Params> = {
  id: string
  template_id: string
  params: Params
  ratings: RankEvalRequestRating[]
}

type RankEvalRequestTemplate = {
  id: string
  templates: {
    inline: unknown
  }
}

export type RankEvalRequest<TemplateParams> = {
  templates: RankEvalRequestTemplate[]
  requests: RankEvalRequestRequest<TemplateParams>[]
  metric: unknown
}

export type RankEvalResponsWithMeta = RankEvalResponse & {
  pass: Pass
  // We've set the passes here as I didn't want to augment the original response.
  // There's probably a better way to do this, but it'll do for now.
  passes: Record<string, Pass>
  queryId: string
  index: string
  query: {
    method: string
    path: string
    body: string
  }
}

const rankClient = new Client({
  cloud: {
    id: ES_RANK_CLOUD_ID,
  },
  auth: {
    username: ES_RANK_USER,
    password: ES_RANK_PASSWORD,
  },
})

const ratingClient = new Client({
  cloud: {
    id: ES_RATINGS_CLOUD_ID,
  },
  auth: {
    username: ES_RATINGS_USER,
    password: ES_RATINGS_PASSWORD,
  },
})

export { rankClient, ratingClient }
