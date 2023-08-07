import warnings

import pytest

from .. import nth
from ..models import PrecisionTestCase

test_cases = [
    PrecisionTestCase(
        search_terms="information law",
        expected_ids=["zkg7xqm7"],
        description=(
            "Multi-word exact matches at the start of a title should be "
            "prioritised "
            "https://github.com/wellcomecollection/catalogue-api/issues/466"
        ),
    ),
    PrecisionTestCase(
        search_terms="DJmjW2cU",
        expected_ids=["djmjw2cu"],
        description="Case insensitive IDs",
    ),
    PrecisionTestCase(
        search_terms="2013i",
        expected_ids=["djmjw2cu"],
        description="Reference number as ID",
    ),
    PrecisionTestCase(
        search_terms="2599i",
        expected_ids=["xxskepr5"],
        description="Reference number as ID",
    ),
    PrecisionTestCase(
        search_terms="seq88sr4 qfk4vbp8",
        expected_ids=["seq88sr4", "qfk4vbp8"],
        description="multiple IDs",
    ),
    PrecisionTestCase(
        search_terms="Cassils Time lapse",
        expected_ids=["ftqy78zj"],
        description="Contributor and title in the same query",
    ),
    PrecisionTestCase(
        search_terms="bulloch history of bacteriology",
        expected_ids=["rkcux48q"],
        description="Contributor and title in the same query",
    ),
    PrecisionTestCase(
        search_terms="stim",
        expected_ids=["e8qxq5mv"],
        description=(
            "Exact match on title with lowercasing and punctuation stripping"
        ),
    ),
    PrecisionTestCase(
        search_terms="The Piggle",
        expected_ids=["q4drcxc6"],
        description="Example of a known title's prefix, but not the full thing",
    ),
    PrecisionTestCase(
        search_terms="Das neue Naturheilverfahren",
        expected_ids=["execg22x"],
        description="Example of a known title's prefix, but not the full thing",
    ),
    PrecisionTestCase(
        search_terms="Bills of mortality",
        expected_ids=["xwtcsk93"],
        description="Example of a known title's prefix, but not the full thing",
    ),
    PrecisionTestCase(
        search_terms="L0033046",
        expected_ids=["kmebmktz"],
        description="Miro ID matching",
    ),
    PrecisionTestCase(
        search_terms="kmebmktz",
        expected_ids=["kmebmktz"],
        description="Work ID matching",
    ),
    PrecisionTestCase(
        search_terms="gzv2hhgy",
        expected_ids=["kmebmktz"],
        description="Image ID matching",
    ),
    PrecisionTestCase(
        search_terms="Oxford dictionary of national biography",
        expected_ids=["ruedafcw"],
        description="Example of a known title's prefix, but not the full thing",
    ),
    PrecisionTestCase(
        search_terms="Hunterian wa/hmm",
        expected_ids=["f3gpbk74"],
        description="archive reference number and a word from the title",
    ),
    PrecisionTestCase(
        search_terms="mammas favorites",
        expected_ids=["dbqsn5gk"],
        description=(
            "Searching without punctuation should match a document with "
            "punctuation"
        ),
    ),
    PrecisionTestCase(
        search_terms="mamma's favorites",
        expected_ids=["dbqsn5gk"],
        description=(
            "Searching with punctuation should match a document with "
            "punctuation"
        ),
    ),
    PrecisionTestCase(
        search_terms="mamma favorites",
        expected_ids=["dbqsn5gk"],
        description=(
            "Searching for a token without its possessive should match a "
            "document with"
        ),
    ),
    PrecisionTestCase(
        search_terms="sophies shell",
        expected_ids=["gdfhp4gw"],
        description=(
            "Searching without punctuation should match a document "
            "with punctuation"
        ),
    ),
    PrecisionTestCase(
        search_terms="sophie's shell",
        expected_ids=["gdfhp4gw"],
        description=(
            "Searching for a term including an apostrophe should match the "
            "same term"
        ),
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
    "test_case", [test_case.param for test_case in test_cases]
)
def test_precision(test_case: PrecisionTestCase, pipeline_client, works_search):
    response = pipeline_client.search(
        **works_search(test_case.search_terms),
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
