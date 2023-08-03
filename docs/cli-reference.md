# `rank`

A CLI for measuring search relevance

**Usage**:

```console
$ rank [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `index`: Manage the rank cluster and its indexes
* `test`: Run tests for the rank CLI

## `rank index`

Manage the rank cluster and its indexes

**Usage**:

```console
$ rank index [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `hello`: hello world

### `rank index hello`

hello world

**Usage**:

```console
$ rank index hello [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `rank test`

Run tests for the rank CLI

**Usage**:

```console
$ rank test [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--test-id TEXT`
* `--content-type [images|works]`
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
