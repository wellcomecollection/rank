import json

import pytest

from . import get_pipeline_elastic_client, works_index, works_query

client = get_pipeline_elastic_client()

test_cases = [
    pytest.param("horse", "pgwnkf2h", id="horse"),
    pytest.param("cow", "wm8wy47d", id="cow"),
]


@pytest.mark.parametrize("search_terms, expected_id", test_cases)
def test_precision(search_terms, expected_id):
    populated_query_string = works_query.replace("{{query}}", search_terms)
    populated_query = json.loads(populated_query_string)
    response = client.search(index=works_index, query=populated_query)
    first_id = response["hits"]["hits"][0]["_id"]
    if first_id != expected_id:
        pytest.fail(f"Expected {expected_id}, got {first_id}", pytrace=False)
