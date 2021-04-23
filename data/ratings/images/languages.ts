export default {
  examples: [
    { query: 'arbeiten', ratings: ['sr4kxmk3', 'utbtee43'] },
    { query: 'conosco', ratings: ['nnh3nh47'] },
    { query: 'allons', ratings: ['dqnapkdx'] },
  ],
  metric: {
    recall: {
      // The relevant_rating_threshold is not used for now as all ratings are marked as 3 in api/eval.ts
      relevant_rating_threshold: 3,
      k: 100,
    },
  },
}
