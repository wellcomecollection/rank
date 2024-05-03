# Search relevance tips and tricks

### Why is this thing showing up rather than this other thing I expect?

Use the [explain API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-explain.html) on your unexpectedly-high-ranking document (easiest to do this in Kibana dev tools) and look for unusually high-scoring subqueries. Sometimes it's useful to `explain` an expected result, too, so you can see what the scores "should" look like. 

This sort of issue will frequently be to do with things being boosted unexpectedly - the ID queries are particularly guilty of causing issues, as they are very strongly boosted.

### How can I make this query faster?

Use the [search profiler](https://www.elastic.co/guide/en/kibana/current/xpack-profiler.html) to see which bits of it are slow. If slowness is evenly distributed across parts of the query, then look for mitigations to reduce the work needed to analyse a query.

### The relevance tests are passing but nobody is happy with the search results! What do I do?

It's easy to for the relevance tests to overfit for specific examples, and to end up with tests per "feature" of search rather than multiple tests for normal, boring, expected behaviour. Add more tests for expected searches, and don't be afraid to mark some more niche tests as known failures.

### Can I solve my problems by tweaking [free parameters](https://en.wikipedia.org/wiki/Free_parameter)?

No - stop it. Boosts, tie-breakers, and other numerical free parameters can be useful for expressing a hierarchy of fields or queries ("value contributors over descriptions") but chasing a suite of passing tests by tweaking them has wasted our time and solved very few problems before. 




