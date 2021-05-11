import { Rating } from '../../types'
import { eq1 } from './pass'

const ratings: Record<string, Rating> = {
  precision: {
    pass: eq1,
    examples: [
      { query: 'crick dna sketch', ratings: ['gzv2hhgy'] },
      { query: 'gzv2hhgy', ratings: ['gzv2hhgy'] },
      { query: 'kmebmktz', ratings: ['gzv2hhgy'] }, // search for work ID and get associated images
      { query: 'L0033046', ratings: ['gzv2hhgy'] },
    ],
    metric: {
      precision: {
        relevant_rating_threshold: 3,
        k: 1,
      },
    },
  },
  recall: {
    pass: eq1,
    examples: [
      { query: 'horse battle', ratings: ['ud35y7c8'] },
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
          'zw53jx3j',
        ],
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
          'th8c2wan',
        ],
      },
    ],
    metric: {
      recall: {
        relevant_rating_threshold: 3,
        k: 30,
      },
    },
  },
  languages: {
    pass: eq1,
    examples: [
      { query: 'arbeiten', ratings: ['sr4kxmk3', 'utbtee43'] },
      { query: 'conosco', ratings: ['nnh3nh47'] },
      { query: 'allons', ratings: ['dqnapkdx'] },
    ],
    metric: {
      recall: {
        relevant_rating_threshold: 3,
        k: 100,
      },
    },
  },
}

export default ratings
