/* eslint-disable camelcase */
// This should never really be used as you can just use
// "analyzer": "standard"
// it's more if you would like to extend or modify just parts of it
const standard_analyzer = {
  tokenizer: 'standard',
  filter: ['lowercase'],
}

// This analyzer "keeps" the slash, by turning it into
// `__` which isn't removed by the standard tokenizer
const standard_with_slashes_analyzer = {
  ...standard_analyzer,
  char_filter: {
    type: 'mapping',
    mappings: ['/ => __'],
  },
}

export { standard_with_slashes_analyzer }
