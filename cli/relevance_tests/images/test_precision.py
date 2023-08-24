import warnings

import pytest

from .. import nth
from ..models import PrecisionTestCase

test_cases = [
    PrecisionTestCase(
        search_terms="crick dna sketch", expected_ids=["gzv2hhgy"]
    ),
    PrecisionTestCase(
        search_terms="gzv2hhgy",
        expected_ids=["gzv2hhgy"],
        description="image id",
    ),
    PrecisionTestCase(
        search_terms="kmebmktz",
        expected_ids=["gzv2hhgy"],
        description="search for work ID and get associated images",
    ),
    PrecisionTestCase(
        search_terms="L0033046",
        expected_ids=["gzv2hhgy"],
        description="miro ID",
    ),
]


@pytest.mark.parametrize(
    "test_case", [test_case.param for test_case in test_cases]
)
def test_precision(test_case: PrecisionTestCase, client, index, render_query):
    response = client.search(
        index=index,
        query=render_query(test_case.search_terms),
        size=test_case.threshold_position,
        _source=False,
    )
    result_ids = [result["_id"] for result in response["hits"]["hits"]]

    # if any of the expected IDs are missing, raise an error
    try:
        missing_ids = [
            expected_id
            for expected_id in test_case.expected_ids
            if expected_id not in result_ids
        ]
        assert not missing_ids
    except AssertionError:
        pytest.fail(
            f"{missing_ids} not found in the search results: {result_ids}",
        )

    # if an expected ID is between the first n positions and the threshold
    # position, raise a warning
    for expected_id in test_case.expected_ids:
        if result_ids.index(expected_id) > len(test_case.expected_ids):
            warnings.warn(
                f"Result {expected_id} was found in position "
                f"{result_ids.index(expected_id)}, after the "
                f"{nth(len(test_case.expected_ids))} position, but before the "
                f"threshold position ({test_case.threshold_position}).",
                UserWarning,
            )

    # if the test is strict, check whether the order of the first n result IDs
    # matches the order of the expected IDs. If they don't match, raise an error
    if test_case.strict:
        try:
            assert (
                result_ids[: test_case.threshold_position]
                == test_case.expected_ids
            )
        except AssertionError:
            pytest.fail(
                f"The order of the expected IDs {test_case.expected_ids} "
                f"does not match the results: {result_ids}",
            )
