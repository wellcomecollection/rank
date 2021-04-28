/* eslint-disable camelcase */
import { Client } from '@elastic/elasticsearch'

const {
  ES_USER,
  ES_PASSWORD,
  ES_CLOUD_ID,
  ES_RANK_USER,
  ES_RANK_PASSWORD,
  ES_RANK_CLOUD_ID,
  ES_RATINGS_USER,
  ES_RATINGS_PASSWORD,
  ES_RATINGS_CLOUD_ID,
} = process.env

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

export type RankEvalResponse = {
  metric_score: number
  queryId: string
  index: string
  details: Record<string, any>
  query: {
    method: string
    path: string
    body: string
  }
}

const client = new Client({
  cloud: {
    id: ES_CLOUD_ID,
  },
  auth: {
    username: ES_USER,
    password: ES_PASSWORD,
  },
})

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

export { client, rankClient, ratingClient }
