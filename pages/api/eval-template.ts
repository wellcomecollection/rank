import { NextApiRequest, NextApiResponse } from "next";
import rankEval from "../../rank_eval.json";

function getAuthCreds(authHeader: string): { user: string; password: string } {
  const [, base64Creds] = authHeader.split(" ");
  const creds = new Buffer(base64Creds, "base64").toString("utf-8");
  const [user, password] = creds.split(":");
  return {
    user,
    password,
  };
}

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const template = req.body;
  const authCreds =
    req.headers.authorization && typeof req.headers.authorization === "string"
      ? getAuthCreds(req.headers.authorization)
      : undefined;

  const { RANK_EVAL_USER, RANK_EVAL_PASSWORD } = process.env;

  if (
    authCreds &&
    authCreds.user === RANK_EVAL_USER &&
    authCreds.password === RANK_EVAL_PASSWORD
  ) {
    const { ES_USER, ES_PASSWORD, ES_URL } = process.env;
    const rankEvalEnpoint = `https://${ES_URL}/works_prod/_rank_eval`;
    const templateId = template.id;
    const rankEvalRequestsWithNewTemplateId = rankEval.requests.map(
      (request) => ({ ...request, template_id: templateId })
    );
    const newRankEval = {
      ...rankEval,
      requests: rankEvalRequestsWithNewTemplateId,
    };
    console.info({ ...newRankEval, templates: [template] });
    const resp = await fetch(rankEvalEnpoint, {
      method: "POST",
      body: JSON.stringify({ ...newRankEval, templates: [template] }),
      headers: {
        Authorization: `Basic ${Buffer.from(
          `${ES_USER}:${ES_PASSWORD}`
        ).toString("base64")}`,
        "Content-Type": "application/json",
      },
    });
    const json = await resp.json();

    res.statusCode = 200;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify(json));
  } else {
    res.statusCode = 400;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ message: "Come again soon" }));
  }
};
