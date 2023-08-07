import pytest

from ..models import RecallTestCase

test_cases = [
    RecallTestCase(search_terms="horse battle", expected_ids=["ud35y7c8"]),
    RecallTestCase(
        search_terms="everest chest",
        expected_ids=[
            "bt9yvss2",
            "erth8sur",
            "fddgu7pe",
            "qbvq42t6",
            "u6ejpuxu",
            "xskq2fsc",
            "prrq5ajp",
            "zw53jx3j",
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
def test_recall(test_case: RecallTestCase, pipeline_client, images_search):
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
