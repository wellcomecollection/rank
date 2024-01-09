import pytest

from ..models import PrecisionTestCase
from ..executors import do_test_precision

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
        search_terms="UeMqQmB9",
        expected_ids=["uemqqmb9"],
        description="Case insensitive IDs",
    ),
    PrecisionTestCase(
        search_terms="10020i",
        expected_ids=["wwsmsnp9"],
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
        known_failure=True,
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
        expected_ids=["f3gpbk74", "k2y5f657"],
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
    PrecisionTestCase(
        search_terms="The Secrets of Alchemy",
        expected_ids=["rtdee482"],
        description="Case-insensitive partial titles",
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
