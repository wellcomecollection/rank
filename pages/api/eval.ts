import { Env, Example } from "../../types";
import { NextApiRequest, NextApiResponse } from "next";
import { Template, getSearchTemplates } from "../../services/search-templates";
import { client } from "../../services/elasticsearch";
import { indexToQueryType } from "../index";

function formatExamples(
  examples: Example[],
  index: string,
  templateId: string
) {
  return examples.map((example: Example) => {
    return {
      id: example.query,
      template_id: templateId,
      params: {
        query: example.query,
      },
      ratings: example.ratings.map((id) => {
        return {
          _id: id,
          _index: index,
          rating: 3,
        };
      }),
    };
  });
}

export type RankEvalResponse = {
  metric_score: number;
  queryId: string;
  index: string;
  details: Record<string, any>;
  query: {
    method: string;
    path: string;
    body: string;
  };
};

const ratingsData = {
  works: ["precision", "recall"],
  images: ["precision", "recall"],
};

export function rankEvalRequests(
  template: Template
): Promise<RankEvalResponse>[] {
  const queryType = indexToQueryType(template.index);
  const requests = ratingsData[queryType].map((moduleName) => {
    return rankEvalRequest(template, moduleName);
  });

  return requests;
}

export async function rankEvalRequest(
  template: Template,
  moduleName: string
): Promise<RankEvalResponse> {
  const queryType = indexToQueryType(template.index);
  const { default: ratings } = await import(
    `../../data/ratings/${queryType}/${moduleName}`
  );
  const requests = formatExamples(
    ratings.examples,
    template.index,
    template.id
  );

  const body = {
    requests,
    templates: [
      {
        id: template.id,
        template: template.template,
      },
    ],
    metric: ratings.metric,
  };

  return client
    .rankEval<RankEvalResponse>({
      index: template.index,
      body,
    })
    .then((resp) => {
      return {
        ...resp.body,
        queryId: template.id,
        index: template.index,
        query: {
          method: "POST",
          path: `${template.index}/_rank_eval`,
          body: JSON.stringify(resp.body),
        },
      };
    });
}

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const env = req.query.env ? req.query.env : "prod";
  const searchTemplates = await getSearchTemplates(env as Env);

  // we allow for multiple requests to be made, because we're testing multiple
  // metrics against multiple indexes
  // see: https://github.com/elastic/elasticsearch/issues/51680
  const requests = searchTemplates.templates
    .map((searchTemplate) => {
      return rankEvalRequests(searchTemplate);
    })
    .reduce((cur, acc) => {
      return cur.concat(acc);
    }, []);

  const responses = await Promise.all(requests);
  const response = {
    pass: responses.every((resp) => resp.metric_score === 1),
    rankings: responses,
  };

  res.statusCode = 200;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(response));
};
