export default {
  mappings: {
    _doc: {
      dynamic: 'strict',
      properties: {
        data: {
          dynamic: 'false',
          properties: {
            alternativeTitles: {
              type: 'text',
              fields: {
                arabic: {
                  type: 'text',
                  analyzer: 'arabic_analyzer',
                },
                bengali: {
                  type: 'text',
                  analyzer: 'bengali_analyzer',
                },
                english: {
                  type: 'text',
                  analyzer: 'english_analyzer',
                },
                french: {
                  type: 'text',
                  analyzer: 'french_analyzer',
                },
                german: {
                  type: 'text',
                  analyzer: 'german_analyzer',
                },
                hindi: {
                  type: 'text',
                  analyzer: 'hindi_analyzer',
                },
                italian: {
                  type: 'text',
                  analyzer: 'italian_analyzer',
                },
                keyword: {
                  type: 'keyword',
                  normalizer: 'lowercase_normalizer',
                },
                shingles: {
                  type: 'text',
                  analyzer: 'shingle_asciifolding_analyzer',
                },
              },
            },
            collectionPath: {
              properties: {
                depth: {
                  type: 'token_count',
                  analyzer: 'standard',
                },
                label: {
                  type: 'text',
                  fields: {
                    keyword: {
                      type: 'keyword',
                    },
                  },
                  analyzer: 'asciifolding_analyzer',
                },
                path: {
                  type: 'text',
                  fields: {
                    keyword: {
                      type: 'keyword',
                    },
                  },
                  copy_to: ['data.collectionPath.depth'],
                  analyzer: 'path_hierarchy_analyzer',
                },
              },
            },
            contributors: {
              properties: {
                agent: {
                  properties: {
                    label: {
                      type: 'text',
                      fields: {
                        keyword: {
                          type: 'keyword',
                        },
                      },
                      analyzer: 'asciifolding_analyzer',
                    },
                  },
                },
              },
            },
            description: {
              type: 'text',
              fields: {
                english: {
                  type: 'text',
                  analyzer: 'english',
                },
              },
            },
            duration: {
              type: 'integer',
            },
            edition: {
              type: 'text',
            },
            format: {
              properties: {
                id: {
                  type: 'keyword',
                },
              },
            },
            genres: {
              properties: {
                concepts: {
                  properties: {
                    label: {
                      type: 'text',
                      fields: {
                        keyword: {
                          type: 'keyword',
                        },
                      },
                      analyzer: 'asciifolding_analyzer',
                    },
                  },
                },
                label: {
                  type: 'text',
                  fields: {
                    keyword: {
                      type: 'keyword',
                    },
                  },
                  analyzer: 'asciifolding_analyzer',
                },
              },
            },
            imageData: {
              properties: {
                id: {
                  properties: {
                    canonicalId: {
                      type: 'keyword',
                      normalizer: 'lowercase_normalizer',
                    },
                    sourceIdentifier: {
                      dynamic: 'false',
                      properties: {
                        value: {
                          type: 'keyword',
                          normalizer: 'lowercase_normalizer',
                        },
                      },
                    },
                  },
                },
              },
            },
            items: {
              properties: {
                id: {
                  properties: {
                    canonicalId: {
                      type: 'keyword',
                      normalizer: 'lowercase_normalizer',
                    },
                    otherIdentifiers: {
                      properties: {
                        value: {
                          type: 'keyword',
                          normalizer: 'lowercase_normalizer',
                        },
                      },
                    },
                    sourceIdentifier: {
                      dynamic: 'false',
                      properties: {
                        value: {
                          type: 'keyword',
                          normalizer: 'lowercase_normalizer',
                        },
                      },
                    },
                  },
                },
                locations: {
                  properties: {
                    accessConditions: {
                      properties: {
                        status: {
                          properties: {
                            type: {
                              type: 'keyword',
                            },
                          },
                        },
                      },
                    },
                    license: {
                      properties: {
                        id: {
                          type: 'keyword',
                        },
                      },
                    },
                    locationType: {
                      properties: {
                        id: {
                          type: 'keyword',
                        },
                      },
                    },
                    type: {
                      type: 'keyword',
                    },
                  },
                },
              },
            },
            languages: {
              properties: {
                id: {
                  type: 'keyword',
                },
                label: {
                  type: 'text',
                  fields: {
                    keyword: {
                      type: 'keyword',
                    },
                  },
                  analyzer: 'asciifolding_analyzer',
                },
              },
            },
            lettering: {
              type: 'text',
              fields: {
                arabic: {
                  type: 'text',
                  analyzer: 'arabic_analyzer',
                },
                bengali: {
                  type: 'text',
                  analyzer: 'bengali_analyzer',
                },
                english: {
                  type: 'text',
                  analyzer: 'english_analyzer',
                },
                french: {
                  type: 'text',
                  analyzer: 'french_analyzer',
                },
                german: {
                  type: 'text',
                  analyzer: 'german_analyzer',
                },
                hindi: {
                  type: 'text',
                  analyzer: 'hindi_analyzer',
                },
                italian: {
                  type: 'text',
                  analyzer: 'italian_analyzer',
                },
                shingles: {
                  type: 'text',
                  analyzer: 'shingle_asciifolding_analyzer',
                },
              },
            },
            notes: {
              properties: {
                content: {
                  type: 'text',
                  fields: {
                    english: {
                      type: 'text',
                      analyzer: 'english',
                    },
                  },
                },
              },
            },
            otherIdentifiers: {
              properties: {
                value: {
                  type: 'keyword',
                  normalizer: 'lowercase_normalizer',
                },
              },
            },
            physicalDescription: {
              type: 'text',
              fields: {
                english: {
                  type: 'text',
                  analyzer: 'english',
                },
                keyword: {
                  type: 'keyword',
                },
              },
            },
            production: {
              properties: {
                agents: {
                  properties: {
                    label: {
                      type: 'text',
                      fields: {
                        keyword: {
                          type: 'keyword',
                        },
                      },
                      analyzer: 'asciifolding_analyzer',
                    },
                  },
                },
                dates: {
                  properties: {
                    label: {
                      type: 'text',
                      fields: {
                        keyword: {
                          type: 'keyword',
                        },
                      },
                      analyzer: 'asciifolding_analyzer',
                    },
                    range: {
                      properties: {
                        from: {
                          type: 'date',
                        },
                      },
                    },
                  },
                },
                function: {
                  properties: {
                    label: {
                      type: 'text',
                      fields: {
                        keyword: {
                          type: 'keyword',
                        },
                      },
                      analyzer: 'asciifolding_analyzer',
                    },
                  },
                },
                label: {
                  type: 'text',
                  fields: {
                    keyword: {
                      type: 'keyword',
                    },
                  },
                  analyzer: 'asciifolding_analyzer',
                },
                places: {
                  properties: {
                    label: {
                      type: 'text',
                      fields: {
                        keyword: {
                          type: 'keyword',
                        },
                      },
                      analyzer: 'asciifolding_analyzer',
                    },
                  },
                },
              },
            },
            subjects: {
              properties: {
                concepts: {
                  properties: {
                    label: {
                      type: 'text',
                      fields: {
                        keyword: {
                          type: 'keyword',
                        },
                      },
                      analyzer: 'asciifolding_analyzer',
                    },
                  },
                },
                label: {
                  type: 'text',
                  fields: {
                    keyword: {
                      type: 'keyword',
                    },
                  },
                  analyzer: 'asciifolding_analyzer',
                },
              },
            },
            title: {
              type: 'text',
              fields: {
                arabic: {
                  type: 'text',
                  analyzer: 'arabic_analyzer',
                },
                bengali: {
                  type: 'text',
                  analyzer: 'bengali_analyzer',
                },
                english: {
                  type: 'text',
                  analyzer: 'english_analyzer',
                },
                french: {
                  type: 'text',
                  analyzer: 'french_analyzer',
                },
                german: {
                  type: 'text',
                  analyzer: 'german_analyzer',
                },
                hindi: {
                  type: 'text',
                  analyzer: 'hindi_analyzer',
                },
                italian: {
                  type: 'text',
                  analyzer: 'italian_analyzer',
                },
                keyword: {
                  type: 'keyword',
                  normalizer: 'lowercase_normalizer',
                },
                shingles: {
                  type: 'text',
                  analyzer: 'shingle_asciifolding_analyzer',
                },
              },
            },
            workType: {
              type: 'keyword',
            },
          },
        },
        deletedReason: {
          dynamic: 'false',
          properties: {
            type: {
              type: 'keyword',
            },
          },
        },
        invisibilityReasons: {
          dynamic: 'false',
          properties: {
            type: {
              type: 'keyword',
            },
          },
        },
        redirect: {
          type: 'object',
          dynamic: 'false',
        },
        state: {
          properties: {
            canonicalId: {
              type: 'keyword',
              normalizer: 'lowercase_normalizer',
            },
            derivedData: {
              dynamic: 'false',
              properties: {
                availableOnline: {
                  type: 'boolean',
                },
                contributorAgents: {
                  type: 'keyword',
                },
              },
            },
            modifiedTime: {
              type: 'date',
            },
            relations: {
              dynamic: 'false',
              properties: {
                ancestors: {
                  properties: {
                    id: {
                      type: 'keyword',
                      normalizer: 'lowercase_normalizer',
                    },
                  },
                },
              },
            },
            sourceIdentifier: {
              dynamic: 'false',
              properties: {
                value: {
                  type: 'keyword',
                  normalizer: 'lowercase_normalizer',
                },
              },
            },
          },
        },
        type: {
          type: 'keyword',
        },
        version: {
          type: 'integer',
        },
      },
    },
  },
}
