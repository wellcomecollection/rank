import { NextApiRequest, NextApiResponse } from "next";
import { client } from "../../services/elasticsearch";
import { getSearchTemplates, Template } from "../../services/search-templates";
import { Env, Example } from "../../types";
import { indexToQueryType } from "../index";

const rankMetric = {
  images: {
    recall: {
      relevant_rating_threshold: 3,
      k: 30,
    },
  },
  works: {
    precision: {
      relevant_rating_threshold: 3,
      k: 1,
    },
  },
};

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

export async function makeRankEvalRequest(
  template: Template
): Promise<RankEvalResponse> {
  const queryType = indexToQueryType(template.index);
  const examples = require(`../../data/ratings/${queryType}.json`);
  const requests = formatExamples(examples, template.index, template.id);

  const body = {
    requests,
    templates: [
      {
        id: template.id,
        template: template.template,
      },
    ],
    metric: rankMetric[queryType],
  };

  const resp = await client.rankEval<RankEvalResponse>({
    index: template.index,
    body,
  });

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
}

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const env = req.query.env ? req.query.env : "stage";
  const searchTemplates = await getSearchTemplates(env as Env);

  // we allow for multiple requests to be made, because each search template
  // might refer to its own index
  const requests = searchTemplates.templates
    .map((searchTemplate) => {
      const requests = makeRankEvalRequest(searchTemplate);
      return requests;
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
