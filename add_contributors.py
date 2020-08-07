from string import punctuation
import requests
import wasabi
import typer
import json
from pathlib import Path

msg = wasabi.Printer()
app = typer.Typer()


def tokenise(name):
    clean_name = name.lower().translate(str.maketrans('', '', punctuation))
    return set(clean_name.split())


def filter_contributors(query, contributors):
    "make sure that there's at least one overlapping token with the query"
    filtered = []
    query_tokens = tokenise(query)
    for contributor in contributors:
        contributor_tokens = tokenise(contributor)
        if query_tokens & contributor_tokens:
            filtered.append(contributor)
    return filtered


@app.command()
def main(query: str = typer.Option(..., prompt=True)):

    contributors = set()
    more_to_fetch = True
    i = 1

    results = []
    with msg.loading(f"Searching for {query}"):
        while more_to_fetch:
            response = requests.get(
                url="https://api.wellcomecollection.org/catalogue/v2/works",
                params={
                    "query": query,
                    "pageSize": 100,
                    "page": i,
                    "include": "contributors"
                }
            ).json()

            results.extend(response["results"])

            if "nextPage" not in response:
                more_to_fetch = False
            i += 1

    for work in results:
        for contributor in work["contributors"]:
            contributors.add(contributor["agent"]["label"])

    typer.echo(
        f"\nFound {len(contributors)} potential contributors in results for \"{query}\""
    )
    contributors = filter_contributors(query, contributors)
    typer.echo(
        f"After filtering out the ones which were obviously wrong, there were {len(contributors)}"
    )

    valid_contributors = set()
    typer.echo("\nWhich contributors are you looking for?")
    for contributor in sorted(list(contributors)):
        if typer.confirm(contributor):
            valid_contributors.add(contributor)

    typer.echo(f"\nYou've chosen {len(valid_contributors)} valid contributors")

    work_ids = set()
    for work in results:
        for contributor in work["contributors"]:
            if contributor["agent"]["label"] in valid_contributors:
                work_ids.add(work["id"])

    typer.echo(f"I found {len(work_ids)} works tagged with those contributors")
    if typer.confirm("Do you want to add them to rank_eval_contributors.json?"):

        with open("rank_eval_contributors.json", "r") as f:
            rank_eval_data = json.load(f)

        rank_eval_data["requests"].append(
            {
                "id": "_".join(query.lower().split()),
                "template_id": "multi_match",
                "params": {
                    "query": query
                },
                "ratings": [
                    {
                        "_id": work_id,
                        "_index": "works_prod",
                        "rating": 3
                    }
                    for work_id in work_ids
                ]
            }
        )

        with open("rank_eval_contributors.json", "w") as f:
            json.dump(rank_eval_data, f)

    msg.good("Done!")


if __name__ == "__main__":
    app()
