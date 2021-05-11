import { RankDetail } from '../../services/elasticsearch'

type Pass = {
  score: number // should be a range between 0 => 1
  pass: boolean
}
type PassFn = (score: RankDetail) => Pass

const eq1: PassFn = (rankDetail: RankDetail) => {
  return {
    score: rankDetail.metric_score,
    pass: rankDetail.metric_score === 1,
  }
}

const eq0: PassFn = (rankDetail: RankDetail) => {
  return {
    score: rankDetail.metric_score,
    pass: rankDetail.metric_score > 0,
  }
}

export { eq0, eq1 }
export type { Pass, PassFn }
