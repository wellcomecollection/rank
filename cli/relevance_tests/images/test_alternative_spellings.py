import pytest

from ..models import RecallTestCase


test_cases = [
    RecallTestCase(
        search_terms="arbeiten",
        expected_ids=["sr4kxmk3", "utbtee43"],
        threshold_position=100,
    ),
    RecallTestCase(
        search_terms="conosco",
        expected_ids=["nnh3nh47"],
        threshold_position=100,
        known_failure=True,
    ),
    RecallTestCase(
        search_terms="allons",
        expected_ids=["dqnapkdx"],
        threshold_position=100,
        known_failure=True,
    ),
]


@pytest.mark.parametrize(
    "test_case", [test_case.param for test_case in test_cases]
)
def test_alternative_spellings(
    test_case: RecallTestCase, pipeline_client, images_search
):
    response = pipeline_client.search(
        **images_search(test_case.search_terms),
        size=test_case.threshold_position,
        _source=False,
    )
    result_ids = [result["_id"] for result in response["hits"]["hits"]]

    try:
        missing_ids = set(test_case.expected_ids) - set(result_ids)
        assert not missing_ids
    except AssertionError:
        pytest.fail(
            f"{missing_ids} not found in the search results: {result_ids}",
        )
