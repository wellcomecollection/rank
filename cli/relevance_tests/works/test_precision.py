import warnings

import pytest

from .. import nth
from ..models import PrecisionTestCase

test_cases = [
    PrecisionTestCase(search_terms="horse", expected_ids=["pgwnkf2h"]),
    PrecisionTestCase(search_terms="cow", expected_ids=["wm8wy47d"]),
    PrecisionTestCase(
        search_terms="duck", expected_ids=["wdh6g4qr", "ard3c5j6", "qjjmrt22"]
    ),
    PrecisionTestCase(
        search_terms="sheep",
        expected_ids=["eegnx7ce"],
        threshold_position=10,
        # should raise a warning, because the expected ID is between the first
        # position and the threshold position
    ),
    PrecisionTestCase(
        search_terms="pig",
        expected_ids=["eegnx7ce"],
        # should fail, because the expected ID isn't in the results
    ),
    PrecisionTestCase(
        search_terms="chicken",
        expected_ids=["utmghxff", "vcxa3w6h"],
        strict=True,
        # should fail, because the expected IDs are both present but are
        # in the wrong order
    ),
    PrecisionTestCase(
        search_terms="information law",
        expected_ids=["zkg7xqm7"],
        description=(
            "Multi-word exact matches at the start of a title should be "
            "prioritised over other single-word matches. See"
            "https://github.com/wellcomecollection/catalogue-api/issues/466"
        ),
    ),
]


@pytest.mark.parametrize(
    "test_case", test_cases, ids=[tc.id for tc in test_cases]
)
def test_precision(test_case: PrecisionTestCase, pipeline_client, works_search):
    response = pipeline_client.search(
        **works_search(test_case.search_terms),
        # only return the necessary number of results to run the tests
        size=test_case.threshold_position,
        # we only need the IDs, so don't return the full documents
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
