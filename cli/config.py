import httpx

search_templates = httpx.get(
    "https://api.wellcomecollection.org/catalogue/v2/search-templates.json"
).json()["templates"]

# the works template is the one which has an index starting with "works"
works_template = next(
    template
    for template in search_templates
    if template["index"].startswith("works")
)

works_index = works_template["index"]
works_query = works_template["query"]

images_template = next(
    template
    for template in search_templates
    if template["index"].startswith("images")
)

images_index = images_template["index"]
images_query = images_template["query"]

pipeline_date = "-".join(works_index.split("-")[-3:])
