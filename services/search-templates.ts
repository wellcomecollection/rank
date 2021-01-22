import { Env } from "../common/components/types";

export type Template = {
  id: string;
  index: string;
  template: { source: { query: Object } };
};

type TemplatesResponse = {
  templates: Template[];
};

type TemplateWithStringQuery = {
  id: string;
  index: string;
  query: string;
};

type TemplatesWithStringQueryResponse = {
  templates: TemplateWithStringQuery[];
};

const endpoints = {
  stage:
    "https://api-stage.wellcomecollection.org/catalogue/v2/search-templates.json",
  prod: "https://api.wellcomecollection.org/catalogue/v2/search-templates.json",
};

async function getSearchTemplates(env: Env): Promise<TemplatesResponse> {
  const res = await fetch(endpoints[env]);
  const json: TemplatesWithStringQueryResponse = await res.json();

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
