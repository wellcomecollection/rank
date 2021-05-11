import { PassFn } from './data/ratings/pass'
import { Metric } from './services/elasticsearch'
import { TemplateSource } from './services/search-templates'

export type QueryType = 'works' | 'images'
export type Env = 'prod' | 'stage'

export type Example = {
  query: string
  ratings: string[]
}

export type Rating = {
  pass: PassFn
  examples: Example[]
  metric: Metric
  searchTemplateAugmentation?: (
    rating: Rating,
    source: TemplateSource
  ) => TemplateSource
}
