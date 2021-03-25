const query = {
  bool: {
    should: [
      {
        multi_match: {
          _name: "identifiers",
          query: "{{query}}",
          fields: [
            "state.canonicalId^1000.0",
            "state.sourceIdentifier.value^1000.0",
            "data.otherIdentifiers.value^1000.0",
            "data.items.id.canonicalId^1000.0",
            "data.items.id.sourceIdentifier.value^1000.0",
            "data.items.id.otherIdentifiers.value^1000.0",
            "data.imageData.id.canonicalId^1000.0",
            "data.imageData.id.sourceIdentifier.value^1000.0",
            "data.imageData.id.otherIdentifiers.value^1000.0",
          ],
          type: "best_fields",
          analyzer: "whitespace_analyzer",
          operator: "Or",
        },
      },
      {
        dis_max: {
          queries: [
            {
              bool: {
                _name: "exact prefix title",
                boost: 1000,
                must: [
                  {
                    prefix: {
                      "data.title.keyword": {
                        value: "{{query}}",
                      },
                    },
                  },
                  // Stops matching prefixes of incomplete words
                  // e.g. query:stim matching:stimulus
                  // But will match "stimming" due to stemming
                  {
                    match_phrase: {
                      "data.title": {
                        query: "{{query}}",
                      },
                    },
                  },
                ],
              },
            },
            {
              multi_match: {
                _name: "exact",
                query: "{{query}}",
                fields: [
                  "data.title^100.0",
                  "data.title.english^100.0",
                  "data.title.shingles^100.0",
                  "data.alternativeTitles^100.0",
                  "data.lettering",
                ],
                type: "best_fields",
              },
            },
            {
              // This is for fields where we expect there to be alternative spellings of words
              // e.g. Arkaprakasa
              multi_match: {
                _name: "alternative spellings",
                query: "{{query}}",
                fields: [
                  "data.title^80.0",
                  "data.title.english^80.0",
                  "data.title.shingles^80.0",
                  "data.alternativeTitles^80.0",
                  "data.lettering",
                ],
                type: "best_fields",
                fuzziness: "AUTO",
                operator: "And",
              },
            },
          ],
        },
      },
      {
        multi_match: {
          _name: "data",
          query: "{{query}}",
          fields: [
            "data.contributors.agent.label^1000.0",
            "data.subjects.concepts.label^10.0",
            "data.genres.concepts.label^10.0",
            "data.production.*.label^10.0",
            "data.description",
            "data.physicalDescription",
            "data.language.label",
            "data.edition",
            "data.notes.content",
            "data.collectionPath.path",
            "data.collectionPath.label",
          ],
          type: "cross_fields",
          operator: "And",
        },
      },
    ],
    filter: [
      {
        term: {
          type: {
            value: "Visible",
          },
        },
      },
    ],
    minimum_should_match: "1",
  },
};

export default query;
