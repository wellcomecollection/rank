import pytest

from collections.abc import Collection

from .models import RecallTestCase, PrecisionTestCase, OrderTestCase


def do_test_recall(
    test_case: RecallTestCase, client, index, render_query, stable_sort_key
):
    expected_ids = set(test_case.expected_ids)
    forbidden_ids = set(test_case.forbidden_ids)
    results = client.search(
        index=index,
        _source=False,
        size=max(test_case.threshold_position, len(expected_ids) + 1),
        query=render_query(test_case.search_terms),
        sort=[{"_score": "desc"}, {stable_sort_key: "asc"}],
    )["hits"]["hits"]
    for doc in results:
        doc_id = doc["_id"]
        try:
            assert doc_id not in forbidden_ids
        except AssertionError:
            pytest.fail(f"Encountered a forbidden ID {doc_id}")
        expected_ids.discard(doc_id)

        if not expected_ids:
            break

    try:
        assert not expected_ids
    except AssertionError:
        pytest.fail(
            f"{expected_ids} not found in the search results",
        )


def do_test_precision(
    test_case: PrecisionTestCase, client, index, render_query, stable_sort_key
):
    expected_ids = test_case.expected_ids
    response = client.search(
        index=index,
        query=render_query(test_case.search_terms),
        sort=[{"_score": "desc"}, {stable_sort_key: "asc"}],
        size=len(expected_ids),
        _source=False,
    )
    result_ids = [result["_id"] for result in response["hits"]["hits"]]

    actual: Collection[str]
    expected: Collection[str]

    if test_case.strict:
        actual = result_ids
        expected = expected_ids
    else:
        actual = set(result_ids)
        expected = set(expected_ids)

    try:
        assert actual == expected
    except AssertionError:
        pytest.fail(
            f"The expected IDs ({expected_ids}) did not match the results ({result_ids})"
        )


def do_test_order(
    test_case: OrderTestCase, client, index, render_query, stable_sort_key
):
    before_ids = set(test_case.before_ids)
    after_ids = set(test_case.after_ids)
    assert not before_ids.intersection(after_ids), (
        "before and after IDs must be disjoint!"
    )

    results = client.search(
        index=index,
        _source=False,
        size=test_case.threshold_position,
        query=render_query(test_case.search_terms),
        sort=[{"_score": "desc"}, {stable_sort_key: "asc"}],
    )["hits"]["hits"]

    failures = []
    for doc in results:
        doc_id = doc["_id"]

        before_ids.discard(doc_id)

        if before_ids and doc_id in after_ids:
            failures.append((before_ids.copy(), doc_id))

        after_ids.discard(doc_id)

        # We don't mind if we don't see the after_ids
        if not before_ids:
            break

    try:
        assert not before_ids
    except AssertionError:
        description = test_case.description or ""
        description_suffix = f"\n\n{description}" if description else ""
        pytest.fail(
            f"{before_ids} not found in search results.{description_suffix}",
            pytrace=False,
        )

    if failures:
        description = test_case.description or ""
        failure_message = [
            description,
            "The following IDs were found in the wrong order: ",
            *[
                f"{after_id} appeared before {', '.join(remaining_before)}"
                for remaining_before, after_id in failures
            ],
        ]
        pytest.fail("\n".join(failure_message), pytrace=False)
