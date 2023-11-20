import pytest

from ..models import RecallTestCase
from ..executors import do_test_recall

test_cases = [
    RecallTestCase(search_terms="horse battle", expected_ids=["ud35y7c8"]),
    RecallTestCase(
        search_terms="everest chest",
        expected_ids=[
            "erth8sur",
            "fddgu7pe",
            "qbvq42t6",
            "u6ejpuxu",
            "xskq2fsc",
        ],
    ),
    RecallTestCase(
        search_terms="Frederic Cayley Robinson",
        expected_ids=[
            "avvynvp3",
            "b286u5hw",
            "dey48vd8",
            "g6n5e53n",
            "gcr92r4d",
            "gh3y9p3y",
            "vmm6hvuk",
            "z894cnj8",
            "cfgh5xqh",
            "fgszwax3",
            "hc4jc2ax",
            "hfyyg6y4",
            "jz4bkatc",
            "khw4yqzx",
            "npgefkju",
            "q3sw6v4p",
            "z7huxjwf",
            "dkj7jswg",
            "gve6469u",
            "kyw8ufwn",
            "r49f89rq",
            "sptagjhw",
            "t6jb62an",
            "tq4qjedt",
            "xkt8av46",
            "yh6evjnu",
            "dvg8e7h5",
            "knc95egk",
            "th8c2wan",
        ],
    ),
]


@pytest.mark.parametrize(
    "test_case", [test_case.param for test_case in test_cases]
)
def test_recall(test_case: RecallTestCase, client, index, render_query):
    return do_test_recall(test_case, client, index, render_query)
