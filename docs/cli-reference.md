# `rank`

A CLI for measuring search relevance

**Usage**:

```console
$ rank [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `index`: Manage indices in the rank cluster
* `query`: Manage local queries
* `search`: Run a search against a candidate index,...
* `task`: Manage tasks running on the rank cluster
* `test`: Run relevance tests

## `rank index`

Manage indices in the rank cluster

**Usage**:

```console
$ rank index [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create an index in the rank cluster
* `delete`: Delete an index
* `get`: Get the mappings and settings for an index...
* `list`: List the indices in the rank cluster
* `replicate`: Replicate an index from a production...
* `update`: Update an index in the rank cluster

### `rank index create`

Create an index in the rank cluster

**Usage**:

```console
$ rank index create [OPTIONS]
```

**Options**:

* `--index TEXT`: The name of the index to create
* `--config-path TEXT`: Path to a json file containing the index settings and mappings. If a config file is not provided, you will be prompted to select one from the index config directory
* `--source-index TEXT`: The name of an existing index to reindex from. If a source index is not provided, you will be prompted to select one from the rank cluster
* `--help`: Show this message and exit.

### `rank index delete`

Delete an index

**Usage**:

```console
$ rank index delete [OPTIONS]
```

**Options**:

* `--index TEXT`: The name of the index to delete. If an index is not provided, you will be prompted to select one from the rank cluster
* `--help`: Show this message and exit.

### `rank index get`

Get the mappings and settings for an index in the rank cluster

**Usage**:

```console
$ rank index get [OPTIONS]
```

**Options**:

* `--index TEXT`: The index to get the mappings and settings for. If an index is not provided, you will be prompted to select one from the rank cluster
* `--help`: Show this message and exit.

### `rank index list`

List the indices in the rank cluster

**Usage**:

```console
$ rank index list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `rank index replicate`

Replicate an index from a production cluster to the rank cluster

**Usage**:

```console
$ rank index replicate [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `rank index update`

Update an index in the rank cluster

**Usage**:

```console
$ rank index update [OPTIONS]
```

**Options**:

* `--index TEXT`: The name of the index to update. If an index is not provided, you will be prompted to select one from the rank cluster
* `--config-path TEXT`: Path to a json file containing the index settings and mappings. If a config file is not provided, you will be prompted to select one from the index config directory
* `--help`: Show this message and exit.

## `rank query`

Manage local queries

**Usage**:

```console
$ rank query [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Get the prod queries from the API
* `list`: List the queries in the query directory

### `rank query get`

Get the prod queries from the API

Useful when you're working on a new relevance requirement, but don't
want to start completely from scratch

N.B. This command will overwrite any existing queries in the query
directory `data/queries`

**Usage**:

```console
$ rank query get [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `rank query list`

List the queries in the query directory

**Usage**:

```console
$ rank query list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `rank search`

Run a search against a candidate index, using a candidate query


Useful when developing a new query or index and looking for qualitative
feedback, rather than the quantitative feedback you get from running
the full rank test suite.


The command will output a table of results with the following columns:

Score, ID, Title, Dates, Reference number

**Usage**:

```console
$ rank search [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--search-terms TEXT`: The search terms to use
* `--index TEXT`: The index to search in
* `--query-path TEXT`: The query to run
* `--n INTEGER RANGE`: The number of results to return  [default: 10; 1<=x<=100]
* `--help`: Show this message and exit.

**Commands**:

* `compare`: Compare the speed of two queries against...
* `get-terms`: Get a list of real search terms for a...

### `rank search compare`

Compare the speed of two queries against the same index

**Usage**:

```console
$ rank search compare [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `rank search get-terms`

Get a list of real search terms for a given content type

**Usage**:

```console
$ rank search get-terms [OPTIONS]
```

**Options**:

* `--content-type [works|images]`: The content type to find real search terms for
* `--help`: Show this message and exit.

## `rank task`

Manage tasks running on the rank cluster

**Usage**:

```console
$ rank task [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `cancel`: Cancel a task
* `list`: List all tasks
* `status`: Get the status of a task

### `rank task cancel`

Cancel a task

**Usage**:

```console
$ rank task cancel [OPTIONS]
```

**Options**:

* `--task TEXT`: Task ID. If not provided, you will be prompted to select an ID from a list of running tasks
* `--help`: Show this message and exit.

### `rank task list`

List all tasks

**Usage**:

```console
$ rank task list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `rank task status`

Get the status of a task

**Usage**:

```console
$ rank task status [OPTIONS]
```

**Options**:

* `--task-id TEXT`: Task ID. If not provided, you will be prompted to select an ID from a list of running tasks
* `--help`: Show this message and exit.

## `rank test`

Run relevance tests

**Usage**:

```console
$ rank test [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--test-id TEXT`
* `--content-type [works|images]`
* `--help`: Show this message and exit.

**Commands**:

* `list`: List all tests that can be run

### `rank test list`

List all tests that can be run

**Usage**:

```console
$ rank test list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
