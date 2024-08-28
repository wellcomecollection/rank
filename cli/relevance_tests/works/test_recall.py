import pytest

from ..models import RecallTestCase
from ..executors import do_test_recall

test_cases = [
    RecallTestCase(
        search_terms="indian journal of medical research 1930-1931",
        expected_ids=["p444t8rp", "kccp8d5t"],
        description=(
            "Query where most search terms (but not all) are in the title"
        ),
    ),
    RecallTestCase(
        search_terms="G.G. Smyth",
        expected_ids=["tkm8r6vk"],
        description="Query where both search terms are needed for meaningful results",
    ),
    RecallTestCase(
        search_terms="Atherosclerosis: an introduction to atherosclerosis",
        expected_ids=["bcwvtknn", "rty8296y"],
        description="Two works with matching titles",
    ),
    RecallTestCase(
        search_terms="1008i 2599i",
        expected_ids=["wbreezks", "xxskepr5"],
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
        expected_ids=["qfdvkegw", "je5pm2gj"],
        description="Archive refno and a word from the description",
    ),
    RecallTestCase(
        search_terms="eugenics society annual reports",
        expected_ids=["k9w95csw", "asqf8kzb", "n499pzsr"],
        description="Matches archives without providing refnos",
        threshold_position=100,
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
    RecallTestCase(
        search_terms="Joint War Committee of the British Red Cross Society and the Order of St. John of Jerusalem in England.",
        expected_ids=["b3b5dvfy"],
        description="Moderately long phrase queries should work, and not time out",
    ),
    RecallTestCase(
        search_terms="The accomplish'd ladies delight, in preserving, physick, beautifying, and cookery. : Containing I. The art of preserving and candying fruits and flowers; and the making of all sorts of conserves, syrups, and jellies. II. The physical cabinet: or, excellent receipts in physick and chirurgery; together with some beautifying waters, to adorn and add loveliness to the face and body: and also some new and excellent receipts relating to the female sex: and for the general good of families, is added the true receipt for making that famous cordial drink Daffy's elixir salutis. III. The compleat cook's guide: or, directions for dressing all sorts of flesh, fowl and fish, both in the English and French mode; with all sorts of sauces and sallets: and the making pyes, pasties, tarts, and custards, with the forms and shapes of many of them.",
        expected_ids=["cve4dn84"],
        description="Extremely long phrase queries should work, and not time out",
    ),
    RecallTestCase(
        search_terms="A true and perfect relation of the whole proceedings against the late most garnerous traitors",
        expected_ids=[],
        forbidden_ids=["r2s5nj96"],
        description="Searches should not return irrelevant images of veterinary ailments",
    ),
    RecallTestCase(
        search_terms="EPB/ENCY",
        expected_ids=[
            "htbq7eqm",
            "ctuhg29m",
            "dsfbdtdz",
            "eznj7hg9",
            "thq463sd",
        ],
        forbidden_ids=[],
        description="A partial slash separated shelfmark search should return results that have a partial matching shelfmark",
    ),
    RecallTestCase(
        search_terms="EPB/ENCY/6.v3 EPB/ENCY/1.v5",
        expected_ids=[
            "htbq7eqm",
            "xu3t38ue",
        ],
        forbidden_ids=[],
        description="Multiple results can be returned for shelfmarks in the same query",
    ),
    RecallTestCase(
        search_terms="i12613290 3324V",
        expected_ids=[
            "xu3t38ue",
            "sweyu7qz",
        ],
        forbidden_ids=[],
        description="IDs and shelfmarks can be mixed in the same query and return results",
    ),
    RecallTestCase(
        search_terms="FTY.S",
        expected_ids=["c5ktw2hd", "tbknvqjq", "xdcn5n25"],
        forbidden_ids=[],
        description="A partial dot separated shelfmark search should return results that have a partial matching shelfmark",
    ),
]


@pytest.mark.parametrize(
    "test_case", [test_case.param for test_case in test_cases]
)
def test_recall(
    test_case: RecallTestCase, client, index, render_query, stable_sort_key
):
    return do_test_recall(
        test_case, client, index, render_query, stable_sort_key
    )
