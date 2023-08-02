import json
import pytest

from .. import get_pipeline_elastic_client, works_index, works_query

from ..models import RecallTestCase

client = get_pipeline_elastic_client()


test_cases = [
    RecallTestCase(
        search_terms="indian journal of medical research 1930-1931",
        expected_ids=["p444t8rp", "kccp8d5t"],
        description="Most search terms (but not all) are in the title",
    ),
    RecallTestCase(
        search_terms="Atherosclerosis: an introduction to atherosclerosis",
        expected_ids=["bcwvtknn", "rty8296y"],
        description="Two works with matching titles",
    ),
    RecallTestCase(
        search_terms="2013i 2599i",
        expected_ids=["djmjw2cu", "xxskepr5"],
        description="Multiple IDs",
    ),
]


@pytest.mark.parametrize(
    "test_case", test_cases, ids=[tc.id for tc in test_cases]
)
def test_recall(test_case: RecallTestCase):
    populated_query = json.loads(
        works_query.replace("{{query}}", test_case.search_terms)
    )
    response = client.search(
        index=works_index,
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
