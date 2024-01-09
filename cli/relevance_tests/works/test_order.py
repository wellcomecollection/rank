import elasticsearch.helpers
import pytest

from ..models import OrderTestCase
from ..executors import do_test_order

test_cases = [
    OrderTestCase(
        search_terms="stimming",
        before_ids=["e8qxq5mv", "uuem7v9a"],
        after_ids=["n323a3a4", "jktm3e74", "frgjdu67"],
        description="Ensure that we return non-typos over typos e.g. query:stimming matches:stimming > swimming",
    ),
    OrderTestCase(
        search_terms="Crète",
        before_ids=["yyz378xr", "d6aezcvw", "z4yefjez"],
        after_ids=["gsehqy4k", "zq2yf7uz", "d2c3k3d3"],
        description="Term with diacritics is scored higher than the asciifolded equivalent, or versions with different diacritics",
        known_failure=True,
    ),
    OrderTestCase(
        search_terms="horse furniture",
        description="Matches ordered terms ahead of unordered terms",
        before_ids=["kdusu63n"],
        after_ids=["uxcxfj9d", "fpeerby9"],
    ),
    OrderTestCase(
        search_terms="everest chest",
        description="Matches titles over descriptions",
        before_ids=["jmt44asm", "p2yucm2e", "pr929v3m"],
        after_ids=["g44jyqgs"],
    ),
    OrderTestCase(
        search_terms="crips",
        description="Pluralised match appears before singular stemmed match",
        before_ids=["sgpyy6gb", "bp45sf6d"],
        after_ids=["ptvgbenh", "r3eue8kw"],
    ),
    OrderTestCase(
        search_terms="crip",
        description="Exact singular match appears before pluralised match",
        before_ids=["ptvgbenh", "r3eue8kw"],
        after_ids=["sgpyy6gb", "bp45sf6d"],
    ),
    OrderTestCase(
        search_terms="CRIPS",
        description="Capitalised match appears before lower case match",
        before_ids=["bp45sf6d", "s949zn4f"],
        after_ids=["ptvgbenh", "sk78b6pr"],
    ),
    OrderTestCase(
        search_terms="AIDS",
        description="Capitalised match appears before lower case match",
        before_ids=["n9xsxzg7", "mr332fhn", "e2w3hc2t", "jfhq5hrv"],
        after_ids=["gvem6rts", "vfwczwr7"],
    ),
    OrderTestCase(
        search_terms="aid",
        description="Matches exact terms before stemmed terms",
        before_ids=["ns8dqqu3", "p8e5jrbk", "whvu96xr"],
        after_ids=["ae6cc6d9", "gvdwhbnd", "er9z8sj4"],
    ),
    OrderTestCase(
        search_terms="aids poster",
        description="Matches ordered terms ahead of unordered terms",
        id="aids poster - ordered terms ahead of unordered terms",
        before_ids=["czgtrmfn", "bry8xyza"],
        after_ids=["e8vnd4s7"],
        known_failure=True,
    ),
    OrderTestCase(
        search_terms="x-ray",
        description="tokens joined by hyphens are matched above tokens which are joined by whitespace",
        before_ids=["maxctjgf", "c3jatdq5", "q8tnjvm8", "gfp86e2b"],
        after_ids=["thgzs6pd"],
    ),
    OrderTestCase(
        search_terms="Mackie",
        before_ids=["k8ccmj6t", "s2tnttyn"],
        after_ids=["ae5kymcs"],
        description="An exact matches in the title should appear before a misspelled match in the contributor and title. Also uses a filter",
        filter={"term": {"query.format.id": "h"}},
    ),
    OrderTestCase(
        search_terms="b16576111",
        before_ids=["zmmbjkja"],
        after_ids=["vburynen", "vgfa9dg6", "wgr6zsnc"],
        description="Source identifiers of works appear before works which are linked to/from",
    ),
]


@pytest.mark.parametrize(
    "test_case", [test_case.param for test_case in test_cases]
)
def test_order(
    test_case: OrderTestCase, client, index, render_query, stable_sort_key
):
    return do_test_order(
        test_case, client, index, render_query, stable_sort_key
    )
