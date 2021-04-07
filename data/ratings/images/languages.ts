export default {
  examples: [],
  metric: {
    recall: {
      // The relevant_rating_threshold is not used for now as all ratings are marked as 3 in api/eval.ts
      relevant_rating_threshold: 3,
      k: 100,
    },
  },
}
