export const ratings = {
  precision: {
    examples: [
      { query: 'Cassils Time lapse', ratings: ['ftqy78zj'] },
      { query: 'stim', ratings: ['e8qxq5mv'] },
      { query: 'bulloch history of bacteriology', ratings: ['rkcux48q'] }, // Contributor and title
      { query: 'stimming', ratings: ['uuem7v9a'] }, // ensure that we return non-typos over typos e.g. query:stimming matches:stimming > swimming
      { query: 'The Piggle', ratings: ['vp7q52gs'] }, // Example of a known title's prefix, but not the full thing
      { query: 'Das neue Naturheilverfahren', ratings: ['execg22x'] },
      { query: 'bills of mortality', ratings: ['xwtcsk93'] },
      { query: 'L0033046', ratings: ['kmebmktz'] },
      { query: 'kmebmktz', ratings: ['kmebmktz'] },
      { query: 'gzv2hhgy', ratings: ['kmebmktz'] },
      {
        query: 'Oxford dictionary of national biography',
        ratings: ['ruedafcw'],
      },
    ],
    metric: {
      precision: {
        relevant_rating_threshold: 3,
        k: 1,
      },
    },
  },
  recall: {
    examples: [
      {
        query: 'Atherosclerosis : an introduction to atherosclerosis',
        ratings: ['bcwvtknn', 'rty8296y'],
      },
    ],
    metric: {
      recall: {
        relevant_rating_threshold: 3,
        k: 5,
      },
    },
  },
  languages: {
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
        relevant_rating_threshold: 3,
        k: 100,
      },
    },
  },
  negative: {
    examples: [
      { query: 'Deptford', ratings: ['pb4rbujd', 'g2awspp9'] }, // shouldn't match "dartford" or "hertford"
      { query: 'Sahagún', ratings: ['neumfv84', 'dzhxzxcr'] }, // shouldn't match "gahagan"
      { query: 'posters', ratings: ['z85jd9f4', 'qpkfxsst'] }, // shouldn't match "porter"
      { query: 'gout', ratings: ['t67v2y55'] }, // shouldn't match "out"
      { query: 'L0062541', ratings: ['wsqmrqfj'] }, // shouldn't match "L0032741" in the title
      { query: 'test', ratings: ['t67v2y55'] },
    ],
    metric: {
      recall: {
        relevant_rating_threshold: 3,
        k: 100000,
      },
    },
  },
}
