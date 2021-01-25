# Adding examples to rank eval

Known examples for rank eval are stored in /data/known-examples, with image examples in `images.json` and works in `works.json`. Each file is a list of examples with the form:

```json
{
  "query": "everest chest",
  "ratings": [
    "bt9yvss2",
    "erth8sur",
    "fddgu7pe",
    "qbvq42t6",
    "u6ejpuxu",
    "xskq2fsc",
    "prrq5ajp",
    "zw53jx3j"
  ]
}
```

`query` is the query that the user sends to the api/search box
`ratings` is a list of expected result work/image IDs. Each example can have multiple target IDs.
