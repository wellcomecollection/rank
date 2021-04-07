const languages = ['french', 'german', 'italian', 'hindi', 'bengali', 'arabic']
const languageQueries = languages.map((language) => {
  const languageQuery = { match: {} }
  languageQuery.match[`data.title.${language}`] = {
    _name: `${language} title`,
    query: '{{query}}',
    analyzer: language
  }
  return languageQuery
})

const query = {
  bool: {
    minimum_should_match: '1',
    should: [
      {
        multi_match: {
          _name: 'identifiers',
          analyzer: 'whitespace_analyzer',
          fields: [
            'state.canonicalId^1000.0',
            'state.sourceIdentifier.value^1000.0',
            'data.otherIdentifiers.value^1000.0',
            'data.items.id.canonicalId^1000.0',
            'data.items.id.sourceIdentifier.value^1000.0',
            'data.items.id.otherIdentifiers.value^1000.0',
            'data.imageData.id.canonicalId^1000.0',
            'data.imageData.id.sourceIdentifier.value^1000.0',
            'data.imageData.id.otherIdentifiers.value^1000.0'
          ],
          operator: 'Or',
          query: '{{query}}',
          type: 'best_fields'
        }
      },
      {
        dis_max: {
          queries: [
            {
              bool: {
                _name: 'title prefix',
                boost: 1000.0,
                must: [
                  {
                    prefix: {
                      'data.title.keyword': {
                        value: '{{query}}'
                      }
                    }
                  },
                  {
                    match_phrase: {
                      'data.title': {
                        query: '{{query}}'
                      }
                    }
                  }
                ]
              }
            },
            {
              multi_match: {
                _name: 'title exact spellings',
                fields: [
                  'data.title^100.0',
                  'data.title.english^100.0',
                  'data.title.shingles^100.0',
                  'data.alternativeTitles^100.0'
                ],
                operator: 'And',
                query: '{{query}}',
                type: 'best_fields'
              }
            },
            {
              multi_match: {
                _name: 'title alternative spellings',
                fields: [
                  'data.title^80.0',
                  'data.title.english^80.0',
                  'data.title.shingles^80.0',
                  'data.alternativeTitles^80.0'
                ],
                fuzziness: 'AUTO',
                operator: 'And',
                query: '{{query}}',
                type: 'best_fields'
              }
            },
            {
              dis_max: {
                _name: 'non-english titles',
                queries: languageQueries
              }
            }
          ]
        }
      },
      {
        multi_match: {
          _name: 'data',
          fields: [
            'data.contributors.agent.label^1000.0',
            'data.subjects.concepts.label^10.0',
            'data.genres.concepts.label^10.0',
            'data.production.*.label^10.0',
            'data.description',
            'data.physicalDescription',
            'data.language.label',
            'data.edition',
            'data.notes.content',
            'data.collectionPath.path',
            'data.collectionPath.label',
            'data.lettering'
          ],
          operator: 'And',
          query: '{{query}}',
          type: 'cross_fields'
        }
      }
    ],
    filter: [
      {
        term: {
          type: {
            value: 'Visible'
          }
        }
      }
    ]
  }
}

export default query
