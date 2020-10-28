import { NextApiRequest, NextApiResponse } from "next";
import { rankRequests, rankMetric } from "../../data/rank";
import { getSearchTemplates } from "../../services/search-templates";

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const { env } = req.query;
  if (env && !(env === "prod" || env === "stage")) {
    throw new Error(`Env cannot be ${env}`);
  }
  const { ES_USER, ES_PASSWORD, ES_URL } = process.env;
  const searchTemplatesResp = await getSearchTemplates(
    env ? env.toString() : undefined
  );
  const rankEvalEnpoint = `https://${ES_URL}/${searchTemplatesResp.templates[0].index}/_rank_eval`;

  const requests = searchTemplatesResp.templates
    .map((template) => {
      return rankRequests(template.index, template.id);
    })
    .reduce((cur, acc) => {
      return cur.concat(acc);
    }, []);

  const body = {
    requests,
    templates: searchTemplatesResp.templates.map((template) => {
      return {
        id: template.id,
        template: template.template,
      };
    }),
    metric: rankMetric,
  };

  const resp = await fetch(rankEvalEnpoint, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      Authorization: `Basic ${Buffer.from(`${ES_USER}:${ES_PASSWORD}`).toString(
        "base64"
      )}`,
      "Content-Type": "application/json",
    },
  });
  const json = await resp.json();
  const success = json.metric_score === 1;

  res.statusCode = 200;
  res.setHeader("Content-Type", "application/json");
  res.end(
    JSON.stringify({
      success,
      ...json,
    })
  );
};
