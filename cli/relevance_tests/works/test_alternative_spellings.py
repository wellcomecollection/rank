import json

import pytest

from .. import get_pipeline_elastic_client, works_index, works_query
from ..models import RecallTestCase

client = get_pipeline_elastic_client()


test_cases = [
    RecallTestCase(
        search_terms="arbeiten",
        expected_ids=["xn7yyrqf"],
        description="german stemming",
        threshold_position=1000,
    ),
    RecallTestCase(
        search_terms="savoire",
        expected_ids=["tbuwy9bk"],
        description="french stemming",
        threshold_position=1000,
    ),
    RecallTestCase(
        search_terms="conosceva",
        expected_ids=["j3w6u4t2", "mt8bj5zk", "vhf56vvz"],
        description="italian stemming",
        threshold_position=1000,
    ),
    RecallTestCase(
        search_terms="sharh",
        expected_ids=["frd5y363"],
        threshold_position=1000,
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="arkaprakāśa",
        expected_ids=["qqh7ydr3", "qb7eggtk", "jvw4bdrz", "jh46tazh"],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="Institvtio Astronomica",
        description="v is folded to match u in the title, but still matches v",
        expected_ids=[
            "f8xmty8b",
            "mk95bet3",
            "ct22shvj",
            "mk74ws8y",
            "k4k3jcvx",
            "yp67jjj5",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="Institutio Astronomica",
        description="u is folded to match v in the title, but still matches u",
        expected_ids=[
            "f8xmty8b",
            "mk95bet3",
            "ct22shvj",
            "mk74ws8y",
            "k4k3jcvx",
            "yp67jjj5",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="Trinvm magicvm",
        description="v is folded to match u in the title, but still matches v",
        expected_ids=[
            "tvpt7vgd",
            "c3r5t5cm",
            "kn5f6cw3",
            "ynjb4wt5",
            "an3txmz3",
            "pzbrggws",
            "zz45ck2v",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="Trinum magicum",
        description="u is folded to match v in the title, but still matches u",
        expected_ids=[
            "tvpt7vgd",
            "c3r5t5cm",
            "kn5f6cw3",
            "ynjb4wt5",
            "an3txmz3",
            "pzbrggws",
            "zz45ck2v",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="de magnis coniunctionibus",
        description="i is folded to match j in the title, but still matches i",
        expected_ids=[
            "aqvdgv6m",
            "puj4hnsf",
            "qa5fa5y5",
            "y6qqmmeb",
            "m3hk4fkz",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="de magnis conjunctionibus",
        description="i is folded to match j in the title, but still matches i",
        expected_ids=[
            "aqvdgv6m",
            "puj4hnsf",
            "qa5fa5y5",
            "y6qqmmeb",
            "m3hk4fkz",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="A closet for ladies and gentlewomen",
        description="w is folded to match vv in the title, but still matches w",
        expected_ids=[
            "dht2cvr4",
            "yqumcexs",
            "hgv9kbbg",
            "gm4xfbud",
            "pt93ab4u",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="A closet for ladies and gentlevvomen",
        description=(
            "vv is folded to match w in the title, but still matches vv"
        ),
        expected_ids=[
            "dht2cvr4",
            "yqumcexs",
            "hgv9kbbg",
            "gm4xfbud",
            "pt93ab4u",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="ioannis",
        description=(
            "i is folded to match j in the publication label, but still "
            "matches i. applies to uppercase characters"
        ),
        expected_ids=[
            "drsebszt",
            "rw79c2br",
            "nubtrxbb",
            "cfxx7kpr",
            "mepptqy2",
            "a4sbkwqg",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="joannis",
        description=(
            "j is folded to match i in the publication label, but "
            "still matches j. applies to uppercase characters"
        ),
        expected_ids=[
            "drsebszt",
            "rw79c2br",
            "nubtrxbb",
            "cfxx7kpr",
            "mepptqy2",
            "a4sbkwqg",
        ],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="neuues",
        description="uu is folded to match w and vv in the title",
        expected_ids=["ker2t6s4", "m9rdjx58", "nu5dyw37"],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="nevves",
        description="uu is folded to match w and vv in the title",
        expected_ids=["ker2t6s4", "m9rdjx58", "nu5dyw37"],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="newes",
        description="w is folded to match uu and vv in the title",
        expected_ids=["ker2t6s4", "m9rdjx58", "nu5dyw37"],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="al-tibb",
        expected_ids=["t4jqq9ue"],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="Al-ṭibb",
        expected_ids=["t4jqq9ue"],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="nuğūm",
        expected_ids=["m94cyux7"],
    ),
    RecallTestCase(
        threshold_position=1000,
        search_terms="nujum",
        expected_ids=["m94cyux7"],
    ),
]


@pytest.mark.parametrize(
    "test_case", test_cases, ids=[tc.id for tc in test_cases]
)
def test_alternative_spellings(test_case: RecallTestCase):
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
