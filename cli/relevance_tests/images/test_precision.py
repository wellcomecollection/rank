import pytest

from ..models import PrecisionTestCase
from ..executors import do_test_precision

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
def test_precision(
    test_case: PrecisionTestCase, client, index, render_query, stable_sort_key
):
    return do_test_precision(
        test_case, client, index, render_query, stable_sort_key
    )
