import { NextApiRequest, NextApiResponse } from "next";
import searchTemplates from "../../search_templates.json";

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const { query } = req.query;
  const { ES_USER, ES_PASSWORD, ES_URL } = process.env;
  const rankEvalEnpoint = `https://${ES_URL}/works_prod/_search/template`;
  const searchTemplate = searchTemplates.find(
    (template) => template.id === "multi_match"
  );

  const resp = await fetch(rankEvalEnpoint, {
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
