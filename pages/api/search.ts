import { NextApiRequest, NextApiResponse } from "next";
import { getSearchTemplates } from "../../services/search-templates";
import { Env } from "../../common/components/types";

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const { query, env } = req.query;
  const { ES_USER, ES_PASSWORD, ES_URL } = process.env;
  const searchTemplatesResp = await getSearchTemplates(env as Env);
  const searchTemplate = searchTemplatesResp.templates[0];
  const rankEvalEndpoint = `https://${ES_URL}/${searchTemplate.index}/_search/template`;

  const resp = await fetch(rankEvalEndpoint, {
    method: "POST",
    body: JSON.stringify({
      source: searchTemplate.template.source,
      params: {
        query,
      },
    }),
    headers: {
      Authorization: `Basic ${Buffer.from(`${ES_USER}:${ES_PASSWORD}`).toString(
        "base64"
      )}`,
      "Content-Type": "application/json",
    },
  });
  const json = await resp.json();

  const worksResponse = json.hits.hits.map((hit) => {
    return {
      id: hit._id,
      title: hit._source.data.title,
      workType: hit._source.data.workType,
      description: hit._source.data.description,
      contributors: hit._source.data.contributors,
    };
  });

  res.statusCode = 200;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(worksResponse));
};
