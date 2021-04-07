export default {
  examples: [
    { query: 'at-tib', ratings: ['vyqkhbsd'] },
    { query: 'Aṭ-ṭib', ratings: ['vyqkhbsd'] },
    { query: 'nuğūm', ratings: ['nut59kt9'] },
    { query: 'nujum', ratings: ['nut59kt9'] },
    { query: 'arbeiten', ratings: ['xn7yyrqf'] },
    { query: 'travaillons', ratings: ['jb823ud6'] },
    { query: 'conosceva', ratings: ['va2vy7wb'] },
    { query: 'sharh', ratings: ['frd5y363'] }
  ],
  metric: {
    recall: {
      // The relevant_rating_threshold is not used for now as all ratings are marked as 3 in api/eval.ts
      relevant_rating_threshold: 3,
      k: 100
    }
  }
}
