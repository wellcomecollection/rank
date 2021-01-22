import { NextApiRequest, NextApiResponse } from "next";
import { getSearchTemplates, Template } from "../../services/search-templates";
import { Env, QueryType, Example } from "../../common/types";

const { ES_USER, ES_PASSWORD, ES_URL } = process.env;

const rankMetric = {
  images: {
    recall: {
      relevant_rating_threshold: 3,
      k: 25,
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
  return examples.map((example) => {
    return {
      id: example.id,
      template_id: templateId,
      params: {
        query: example.query,
      },
      ratings: example.ratings.map((r) => {
        return {
          _id: r._id,
          _index: index,
          rating: r.rating,
        };
      }),
    };
  });
}

type RankEvalResponse = {
  metric_score: number;
  queryId: string;
  index: string;
};

async function makeRankEvalRequest(
  template: Template
): Promise<RankEvalResponse> {
  // the name of the index should indicate the queryType, eg "images-2021-01-12"
  // should result in an "images" query
  const queryType = template.index.split("-")[0] as QueryType;
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

  const request = {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      Authorization: `Basic ${Buffer.from(`${ES_USER}:${ES_PASSWORD}`).toString(
        "base64"
      )}`,
      "Content-Type": "application/json",
    },
  };

  const rankEvalEndpoint = `https://${ES_URL}/${template.index}/_rank_eval`;
  const response = await fetch(rankEvalEndpoint, request);
  const json: RankEvalResponse = await response.json();

  return {
    ...json,
    queryId: template.id,
    index: template.index,
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
