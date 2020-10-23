import { NextApiRequest, NextApiResponse } from "next";

type TemplatesResponse = {
  templates: Template[];
};

type Template = {
  id: string;
  index: string;
  template: { source: { query: Object } };
};

type TemplateWithStringQuery = {
  id: string;
  index: string;
  query: string;
};

type TemplatesWithStringQueryResponse = {
  templates: TemplateWithStringQuery[];
};

async function getSearchTemplates(): Promise<TemplatesResponse> {
  const endpoint =
    "https://api.wellcomecollection.org/catalogue/v2/search-templates.json";
  const resp = await fetch(endpoint);
  const json: TemplatesWithStringQueryResponse = await resp.json();

  // The query is returned as a string from the API
  const templates: Template[] = json.templates.map((template) => ({
    id: template.id,
    index: template.index,
    template: {
      source: {
        query: JSON.parse(template.query.replace("IdentifiedWork", "Visible")),
      },
    },
  }));
  return { templates };
}

export { getSearchTemplates };
