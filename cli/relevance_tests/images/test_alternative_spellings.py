import pytest

from ..models import RecallTestCase
from ..executors import do_test_recall

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
    test_case: RecallTestCase, client, index, render_query, stable_sort_key
):
    return do_test_recall(test_case, client, index, render_query, stable_sort_key)
