import { NextApiRequest, NextApiResponse } from "next";
import { client } from "../../../services/elasticsearch";
import {
  getSearchTemplates,
  Template,
} from "../../../services/search-templates";
import { makeRankEvalRequest } from "../eval";

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

  const template = queryId
    ? await getTestQuery(queryId.toString())
    : await getCurrentQuery();

  const rankEvalReq = makeRankEvalRequest(template);
  const searchReq = client.searchTemplate({
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

  const [searchResp, rankEvalResp] = await Promise.all([
    searchReq,
    rankEvalReq,
  ]);

  res.statusCode = 200;
  res.setHeader("Content-Type", "application/json");
  res.end(
    JSON.stringify({
      ...searchResp.body,
      rankEval: rankEvalResp,
    })
  );
};
