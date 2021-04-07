export default {
    examples: [
      {
        query: 'everest chest',
        ratings: [
          'bt9yvss2',
          'erth8sur',
          'fddgu7pe',
          'qbvq42t6',
          'u6ejpuxu',
          'xskq2fsc',
          'prrq5ajp',
          'zw53jx3j'
        ]
      },
      {
        query: 'Frederic Cayley Robinson',
        ratings: [
          'avvynvp3',
          'b286u5hw',
          'dey48vd8',
          'g6n5e53n',
          'gcr92r4d',
          'gh3y9p3y',
          'vmm6hvuk',
          'z894cnj8',
          'cfgh5xqh',
          'fgszwax3',
          'hc4jc2ax',
          'hfyyg6y4',
          'jz4bkatc',
          'khw4yqzx',
          'npgefkju',
          'q3sw6v4p',
          'z7huxjwf',
          'dkj7jswg',
          'gve6469u',
          'kyw8ufwn',
          'r49f89rq',
          'sptagjhw',
          't6jb62an',
          'tq4qjedt',
          'xkt8av46',
          'yh6evjnu',
          'dvg8e7h5',
          'knc95egk',
          'th8c2wan'
        ]
      }
    ],
    metric: {
      recall: {
        // The relevant_rating_threshold is not used for now as all ratings are marked as 3 in api/eval.ts
        relevant_rating_threshold: 3,
        k: 100
      }
    }
  }
  