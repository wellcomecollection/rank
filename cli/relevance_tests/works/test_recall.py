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
        search_terms=":(Young Arthur 1741 1820 Rural oeconomy or Essays on the practical parts of husbandry Designed to explain several of the most important methods of conducting farms of various kinds including many useful hints to gentlemen farmers relative to the oeconomical management of their business Containing among other enquiries of that proportioned farm which is of all others the most profitable The best method of conducting farms that consist all of grass or all of arable land The means of keeping the most cattle the year round on a given quantity of land The cheapest way of manuring land Considerations on the oeconomical conduct of gentlemen farmers The comparative profit of farming different soils Of experimental agriculture Of the new husbandry Of the management of borders of arable fields Of periodical publications concerning rural oeconomics To which is added The rural Socrates being memoirs of a country philosopher by the author of The farmer s letters Two lines of quotation in Latin",
        expected_ids=["hpnp6nfy"],
        description="Extremely long phrase queries should work, and not time out",
    ),
    RecallTestCase(
        search_terms="A true and perfect relation of the whole proceedings against the late most garnerous traitors",
        expected_ids=[],
        forbidden_ids=["r2s5nj96"],
        description="Searches should not return irrelevant images of veterinary ailments",
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
