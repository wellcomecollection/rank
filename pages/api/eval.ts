import { NextApiRequest, NextApiResponse } from "next";
import rankEval from "../../rank_eval.json";
import searchTemplates from "../../search_templates.json";

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const { ES_USER, ES_PASSWORD, ES_URL } = process.env;
  const rankEvalEnpoint = `https://${ES_URL}/works_prod/_rank_eval`;
  const resp = await fetch(rankEvalEnpoint, {
    method: "POST",
    body: JSON.stringify({ ...rankEval, templates: searchTemplates }),
    headers: {
      Authorization: `Basic ${Buffer.from(`${ES_USER}:${ES_PASSWORD}`).toString(
        "base64"
      )}`,
      "Content-Type": "application/json",
    },
  });
  const json = await resp.json();

  res.statusCode = 200;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(json));
};
