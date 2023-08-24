# Principles / FAQs

## Why does the rank cluster exist?

When we first started working on search relevance, we had a single cluster that was used for both prod queries and relevance development, among other things. When we started to scale up the number of relevance tests we were running, we found that the cluster occasionally struggled to handle the load from dozens of test queries, alongside real user traffic. This was especially true with experimental queries which were sometimes very expensive to run.

This extra pressure on the cluster would either cause the relevance tests to fail non-deterministically, or worse, cause real user queries to fail. Usually, both happened.

We decided to split the clusters to avoid this problem. The rank cluster is smaller than the pipeline cluster(s), but it is dedicated to relevance testing. Keeping it isolated from the pipeline cluster means that that we can run as many tests as we want without worrying about impacting real users.

## Is it better to have a complicated query or mapping? Where should the complexity live?

The long term goal should always be to move complexity into the mapping.

This can seem counterintuitive for a few reasons:

- Mapping changes (and corresponding reindexes) are _much_ more expensive to test and deploy than query changes
- The query allows for much more logical expressivity than the mapping
- As a result, it's also much easier to reason about problems in the query than the mapping

For those reasons, it's often tempting to load all the complexity in the query, especially when you're just starting development for a new search intention. However, the query is easily bloated. Past a certain size, it can be very difficult to maintain/extend when new search intentions are added.

Query complexity can also lead to much more expensive individual queries. While a reindex with many complicated fields might be hugely expensive in the short term, it will pay off in the long run by allowing you to write much simpler, faster queries.

If you can simplify the query to a simple `multi_match` across a load of very carefully, intentionally analyzed fields, you'll be in a much better place in the long run.

A typical workflow when developing a new mapping/query might look something like this:

- Start with a simple query which fails the target test case
- Add a bunch of clauses to the query to capture the search intention using the current fields
- Realize that the query is getting too complicated
  - Move some of the complexity into the mapping
  - Reindex the data with the new mapping
  - Repeat
- Prune the mapping and query to remove unnecessary clauses

## Why do you index so many fields with so many different analysers? Won't analysing the same field in so many different ways lead to spurious collisions?

The catalogue data contains text in many languages, and we want to support as many user intentions across these texts as possible.

Despite the possibility of spurious collisions between similar terms in different languages, we've found that indexing the same field with multiple analysers is a net win for relevance. The intuition is that by analysing a user's search terms in every language, we're much more likely to find a match in relevant documents which match the query language, and very unlikely to find matches in irrelevant documents from different languages.

We've observed that this holds in practice, despite the huge potential volume of false positives. Where false positives do exist, they're usually buried under relevant, higher-scoring matches, so they don't usually cause problems for users.

Additionally, stacking multiple analysers together should provide an implicit boost to exactly-matching terms in the query and the document, above terms which are similar, because the exact-matching terms will be analysed the same way by every one of the field's analysers, instead of just a few.

For example, consider a user who searches for `swimming` in this index structure.  
At index-time, we should see english subfields stem the word `swimming` down to `swim`. Other forms of the word (eg. `swims`, `swimmingly`, `swimmer`) will also be stemmed down to `swim`. At the same time, all non-english analysers will leave instances of `swimming` in its original form.  
When the user queries the index for instances of `swimming`, we should see retrieve for `swimming` in english documents (stemming both the query and indexed document to `swim`) AND non-english documents (where query and indexed documents match on `swimming`). Documents which contain other forms of the word will also be matched in the english subfield, but will be lower-scoring than the exact matches, because only the english subfield will be able to contribute to their score.

We haven't (yet) observed a need for identifying the language of the search term and only searching the corresponding fields.

## Do I need to reindex _everything_ when I change the mapping? Can I just run tests with a few documents instead?

Yes! Everything needs to be reindexed when testing new mappings.

Relevance tests need to be run against the entire corpus of documents, not just a few illustrative examples. Scoring can behave quite unpredictably at the margins, and you might end up with false positives if you only run tests against a few documents.

Knowing that a match is high-scoring among test documents is not enough to know that it will be high-scoring in production. For example, it's not always enough to know that document `a` appears before documents `b`, `c`, and `d`, if they're all going to be buried under pages of higher-scoring matches which you hadn't anticipated.

Search relevance tuning is an empirical process, and a theoretical solution won't always work as expected when applied to real data. Scores are highly dependent on the underlying dataset (putting it bluntly, just think about how important the IDF is in TF-IDF!).

We also have a lot of _weird_ stuff in the catalogue, and the best (or only) way to know that a mapping will work for the full range of texts is to test it against everything. It's quite common to develop a new mapping, test it successfully with a few documents, and then have a reindex fail on the millionth document. It's much better to find issues like this in the rank environment before pushing the mapping over to the production pipeline.

## How should user feedback be translated into relevance tests?

Most often, feedback on search relevance arrives in the `#wc-platform-feedback` slack channel or emails to `digital@wellcomecollection.org`. Messages might include the user's search terms, the documents they expected to see, and the documents they saw instead. If they don't include all of this information, it's worth asking for it. It's also worth reproducing the search yourself to see if the problem is one which we already know about.

Adding the example to the list of tests directly is usually quite straightforward. If it's possible, including a link to the original discussion in the test description is helpful for future reference.

If the example is obviously a symptom of a broader issue, it can be helpful to go hunting for a few more examples of the behaviour yourself. Padding out the test suite with a few more examples of similar behaviour will help to solve the issue robustly and make future regressions less likely.

It's also worth considering whether there are any inverse examples which could be added to the test suite.

## Why does rank run in CI?

We run rank against the production APIs on a regular schedule to ensure that search is performing as expected. It also alerts us to any changes in the underlying data which might cause a test to fail. Failures are reported to the `#wc-search-alerts` slack channel.

We also run rank against the staging API for PRs to ensure that changes to the mapping/query (or elsewhere) don't cause any regressions in relevance quality.
