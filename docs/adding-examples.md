# Adding examples to rank eval

Known examples for rank eval are stored in /data/known-examples, with image examples in `images.json` and works in `works.json`. Each file is a list of examples with the form:

```json
{
  "id": "title_contrib_bulloch",
  "query": "bulloch history of bacteriology",
  "ratings": [
    {
      "_id": "rkcux48q",
      "rating": 3
    }
  ]
}
```

`id` should be a unique id for each example
`query` is the query that the user sends to the api/search box
`ratings` is a list of expected results, with an `_id` and a `rating`, where `_id` is the work/image id, and `rating` is a measure of how high the work/image should appear in the list of results.

Each example can have multiple target `_id`s.
