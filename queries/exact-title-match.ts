const query = {
  bool: {
    should: [
      {
        prefix: {
          "data.title.keyword": {
            _name: "exact_title",
            value: "{{query}}",
            boost: 1000,
          },
        },
      },
      {
        multi_match: {
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
        multi_match: {
          query: "{{query}}",
          fields: [
            "data.title^100.0",
            "data.title.english^100.0",
            "data.title.shingles^100.0",
            "data.alternativeTitles^100.0",
            "data.lettering",
          ],
          type: "best_fields",
          fuzziness: "AUTO",
          operator: "And",
        },
      },
      {
        multi_match: {
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
