export default {
  examples: [
    {
      query: 'horse battle',
      ratings: ['ud35y7c8'],
    },
    {
      query: 'crick dna sketch',
      ratings: ['gzv2hhgy'],
    },
    {
      query: 'gzv2hhgy',
      ratings: ['gzv2hhgy'],
    },
    {
      // search for work ID and get associated images
      query: 'kmebmktz',
      ratings: ['gzv2hhgy'],
    },
    {
      query: 'L0033046',
      ratings: ['gzv2hhgy'],
    },
  ],
  metric: {
    precision: {
      // The relevant_rating_threshold is not used for now as all ratings are marked as 3 in api/eval.ts
      relevant_rating_threshold: 3,
      k: 1,
    },
  },
}
