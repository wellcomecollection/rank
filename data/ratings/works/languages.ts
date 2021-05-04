export default {
  examples: [
    { query: 'at-tib', ratings: ['qmm9mauk'] },
    { query: 'Aṭ-ṭib', ratings: ['qmm9mauk'] },
    { query: 'nuğūm', ratings: ['jtbenqbq'] },
    { query: 'nujum', ratings: ['jtbenqbq'] },
    { query: 'arbeiten', ratings: ['xn7yyrqf'] },
    { query: 'travaillons', ratings: ['jb823ud6'] },
    { query: 'conosceva', ratings: ['va2vy7wb'] },
    { query: 'sharh', ratings: ['frd5y363'] },
    {
      query: 'arkaprakāśa',
      ratings: ['qqh7ydr3', 'qb7eggtk', 'jvw4bdrz', 'jh46tazh'],
    },
  ],
  metric: {
    recall: {
      // The relevant_rating_threshold is not used for now as all ratings are marked as 3 in api/eval.ts
      relevant_rating_threshold: 3,
      k: 100,
    },
  },
}
