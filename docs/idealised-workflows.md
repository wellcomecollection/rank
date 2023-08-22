# Idealised workflows

This document gives a few illustrative examples of how one might use the rank CLI to develop and test search relevance.

## 1. User describes a new relevance requirement

A user approaches the platform team with a problem: Maybe they expect to see a particular result at the top of the results list for a given set of search terms, but it's not there. Maybe they're seeing a result that they don't expect to see at all. Maybe the results are relevant, but they're not in the order that the user expects.

These requirements should be translated into a set of relevance tests, and added to the rank test suite.

The tests are grouped by the kind of relevance requirement they're testing. For example, if the user expects to see a particular result at the top of the results list, then the test should be added to the `precision` group. If the user expects to see a particular result in the list of results but doesn't care where, then the test should be added to the `recall` group. Each group of tests is stored in a separate file in the `data/tests` directory. Each runs a different set of assertions against the results of a search, with the parameters for the searches defined by each test case.

While a solution is being developed, the new test(s) should be marked as a `known_failure`, which will allow the suite as a whole to pass, while the individual test fails.

## 2. Developing a solution

There are two major components of search which can be tunes: an index mapping (which defines the structure of the inverted index in elasticsearch), and a query (which defines how the search terms are mapped to terms in the index, and how documents are scored against one another).

Most changes to search relevance will involve changes to _both_ of these components. The rank CLI provides commands for developing and testing both.

If your problem is solveable without changes to the index mapping, then you can skip to [Developing a new query](#developing-a-new-query).

### Getting a copy of the production index config for testing

Although elasticsearch is pretty efficient, the load on a cluster from running tests can be significant, especially with the risk of writing inefficient, long-running queries. For that reason, we maintain a separate environment for testing, which we call the **rank cluster**. Testing against this cluster is cheaper and safer than testing against the resources which back our production services.

Copying indexes is an expensive process, so we only do it when we need to. If you're developing a new index mapping, you'll need to copy the production index to the rank cluster. This can be done by running the following command:

```console
rank index replicate
```

You'll be prompted to select the index you want to copy, and to give the new index a name. The new index will be created in the rank cluster, and will be available for searching as soon as the reindex is complete. You can monitor the task's progress by running:

```console
rank task status
```

Again, you'll be prompted to select the task you want to monitor.

### Developing a new index mapping

It's usually helpful to use the existing index configuration (mappings + settings) as a starting point when developing something new. At least, it might help you determine where problems are coming from, and how to avoid making the same mistakes again. You can fetch a copy of the configuration for your newly-replicated index by running:

```console
rank index get
```

You'll be prompted to select the index whose config you want to fetch. The mappings and settings will be saved to a file in the `data/index_config` directory. Edit this file to make your changes, then run:

```console
rank index create
```

You'll be prompted to supply a name for the index, and to select the local index config file that you want to apply to it. Elasticsearch will then create the index with the supplied configuration. Creating the index is a very quick process because no documents are being indexed (you've just created the structure of the index without putting any data in it). You'll then be prompted to start a reindex task, which will copy the data from your source index into the new index structure.

Again, you can check the progress of your reindex task by running:

```console
rank task status
```

and selecting the task with a description like `indices:data/write/reindex`.

If you're not satisfied with the results of your changes, you can delete the index by running:

```console
rank index delete
```

Alternatively, you can edit your index config file, and run

```console
rank index update
```

to apply the changes to the index without deleting it first. This will kick off an `update_by_query` task, which you can monitor in the usual way, looking for tasks with a description like `indices:data/write/update/byquery`. Running an update is most appropriate when you're making small, additive changes to the index config. If you're making more substantial changes, it's usually better to delete the index and start again.

### Developing a new query

If you're not planning to make huge changes to the results, it can be helpful to use an existing query as a starting point. At least, it might help you determine where problems are coming from, and how to avoid making the same mistakes again. You can create local copies of the queries which are running in production by running:

```console
rank query get
```

You'll be prompted to select the query(s) to fetch. The query will be saved as a json file in the `data/queries` directory, which you can edit to make your changes. When you're happy with the changes, you can move on to testing.

## 3. Testing

### Manual queries

The simplest way to test search relevance is to run your new query against the index with some typical search terms, and check whether the results look sensible. You can do this by running

```console
rank search
```

You'll be prompted to choose an index, a query, and to enter some search terms. The results will be printed to the console with links to the full versions of each of the results on wellcomecollection.org. The results should give you a qualitative sense of whether your query is working as expected.

### Automated tests

Over the years, we've used direct feedback from users to amass a large set of search-term / expected-result pairs, which we hope our search API will satisfy. These examples are grouped together into a test suite, which you can run by running:

```console
rank test
```

Instead of manually searching the index and examining the results by hand, the test suite will automatically run and check every requirement, giving an indication of how relevant your query is compared to all of the requirements we know about.

#### Test groups

The tests are grouped into different categories, depending on the kind of relevance requirement they're testing. For example, if the user expects to see a particular result at the top of the results list, then the test should be added to the `precision` group. To run the tests for the precision group alone, you can run:

```console
rank test --group=precision
```

#### Known failures

Relevance is a delicate balancing act, and it's unlikely that a new query will satisfy every requirement perfectly. For that reason, we allow tests to be marked as `known_failures`. These tests will be run as part of the test suite, but they won't cause the suite to fail. They'll be marked as `xfailed` in the report. Continuing to run these tests which we expect to fail allows us to keep track of the requirements we're not satisfying, and to see whether we're making progress towards them.

If you're developing a new query, the test suite will tell you if an known failure has unexpectedly passed (`xpassed`), or if a test that was previously passing has started failing (`failed`).

## 4. Deploying to production

Once you're happy with your changes, you can deploy them in the `catalogue-pipeline` / `catalogue-api` repos! When they changes are live, you should mark the new set of expected failures as `known_failures`, and merge your changes into the `main` branch of this repo, allowing the test suite to pass again.
