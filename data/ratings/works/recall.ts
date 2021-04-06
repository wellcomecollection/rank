export default {
  examples: [
    {
      query: 'sharh',
      ratings: ['frd5y363', 'aarnrbyc']
    },
    {
      query: 'arkaprakāśa',
      ratings: ['qqh7ydr3', 'qb7eggtk', 'jvw4bdrz', 'jh46tazh']
    },
    {
      query: 'Atherosclerosis : an introduction to atherosclerosis',
      ratings: ['bcwvtknn', 'rty8296y']
    }
  ],
  metric: {
    recall: {
      // The relevant_rating_threshold is not used for now as all ratings are marked as 3 in api/eval.ts
      relevant_rating_threshold: 3,
      k: 5
    }
  }
}
