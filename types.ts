import { Metric } from './services/elasticsearch'
import { PassFn } from './data/tests/pass'
import { SearchTemplateSource } from './services/search-templates'

export type QueryType = 'works' | 'images'
export type Env = 'prod' | 'stage'

export type TestCase = {
  query: string
  ratings: string[]
  description?: string
}

export type Test = {
  label: string
  description: string
  pass: PassFn
  cases: TestCase[]
  metric: Metric
  searchTemplateAugmentation?: (
    test: Test,
    source: SearchTemplateSource
  ) => SearchTemplateSource
}
