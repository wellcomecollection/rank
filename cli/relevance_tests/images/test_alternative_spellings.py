import json

import pytest

from .. import get_pipeline_elastic_client, images_index, images_query
from ..models import RecallTestCase

client = get_pipeline_elastic_client()


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
    ),
    RecallTestCase(
        search_terms="allons", expected_ids=["dqnapkdx"], threshold_position=100
    ),
]


@pytest.mark.parametrize(
    "test_case", test_cases, ids=[tc.id for tc in test_cases]
)
def test_alternative_spellings(test_case: RecallTestCase):
    populated_query = json.loads(
        images_query.replace("{{query}}", test_case.search_terms)
    )
    response = client.search(
        index=images_index,
        query=populated_query,
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
