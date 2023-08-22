import pytest

from ..models import RecallTestCase

test_cases = [
    RecallTestCase(
        search_terms="indian journal of medical research 1930-1931",
        expected_ids=["p444t8rp", "kccp8d5t"],
        description=(
            "Query where most search terms (but not all) are in the title"
        ),
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
    RecallTestCase(
        search_terms="wa/hmm durham",
        expected_ids=["euf49qkx", "tpxy78kr", "gu3z98y4", "ad3rfubw"],
        description="Archive refno and a word from the title",
    ),
    RecallTestCase(
        search_terms="wa/hmm benin",
        expected_ids=["qfdvkegw", "je5pm2gj", "dppjjtqz"],
        description="Archive refno and a word from the description",
    ),
    RecallTestCase(
        search_terms="WA/HMM/CM benin",
        expected_ids=["qfdvkegw", "je5pm2gj", "dppjjtqz"],
        description="Archive refno and a word from the description",
    ),
    RecallTestCase(
        search_terms="eugenics society annual reports",
        expected_ids=["k9w95csw", "asqf8kzb", "n499pzsr"],
        description="Matches archives without providing refnos",
        known_failure=True,
    ),
    RecallTestCase(
        search_terms="لكشف",
        expected_ids=["ymnmz59p"],
        description="Matches stemmed arabic text",
        known_failure=True,
    ),
    RecallTestCase(
        search_terms="الكشف",
        expected_ids=["ymnmz59p"],
        description="Matches arabic text",
        known_failure=True,
    ),
    RecallTestCase(
        search_terms="معرفت",
        expected_ids=["a9w79fzj"],
        description="Matches arabic text",
        known_failure=True,
    ),
    RecallTestCase(
        search_terms="عرف",
        expected_ids=["a9w79fzj"],
        description="Matches stemmed arabic text",
        known_failure=True,
    ),
]


@pytest.mark.parametrize(
    "test_case", [test_case.param for test_case in test_cases]
)
def test_recall(test_case: RecallTestCase, client, index, render_query):
    response = client.search(
        index=index,
        query=render_query(test_case.search_terms),
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
