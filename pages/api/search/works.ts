import { Client } from "@elastic/elasticsearch";
import { NextApiRequest, NextApiResponse } from "next";
import {
  getSearchTemplates,
  Template,
} from "../../../services/search-templates";

const { ES_USER, ES_PASSWORD, ES_CLOUD_ID } = process.env;

async function getCurrentQuery(): Promise<Template> {
  const searchTemplates = await getSearchTemplates("prod");
  const template = searchTemplates.templates.find((template) =>
    template.index.startsWith("works")
  );

  return template;
}
async function getTestQuery(id: string): Promise<Template> {
  const currentTemplate = await getCurrentQuery();
  const index = currentTemplate.index;
  const query = await import(`../../../queries/${id}`).then((q) => q.default);

  return {
    id,
    index,
    template: { source: { query: query } },
  };
}

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const { query, queryId } = req.query;

  const client = new Client({
    cloud: {
      id: ES_CLOUD_ID,
    },
    auth: {
      username: ES_USER,
      password: ES_PASSWORD,
    },
  });
  const template = queryId
    ? await getTestQuery(queryId.toString())
    : await getCurrentQuery();

  const resp = await client.searchTemplate({
    index: template.index,
    body: {
      source: {
        ...template.template.source,
        track_total_hits: true,
        highlight: {
          pre_tags: ['<em class="bg-yellow-200">'],
          post_tags: ["</em>"],
          fields: {
            "data.title": { number_of_fragments: 0 },
            "data.contributors.agent.label": { number_of_fragments: 0 },
            "data.subjects.concepts.label": { number_of_fragments: 0 },
            "data.genres.concepts.label": { number_of_fragments: 0 },
          },
        },
      },
      params: {
        query,
      },
    },
  });

  res.statusCode = 200;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(resp.body));
};
