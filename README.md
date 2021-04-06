# Rank

Rank is our source of truth for the goodness of search on wellcomecollection.org.

Rank uses [elasticsearch's `rank_eval` API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-rank-eval.html).

`rank_eval` measures a candidate search algorithm's performance on a set of known search terms against a corresponding set of "expected" results from our catalogue.  

If the candidate algorithms return those results, we know we're meeting a baseline performance requirement. Better scores on those examples should mean better search satisfaction IRL.

## Developing

Run `yarn install` and `yarn dev` to get a local version of the site running
