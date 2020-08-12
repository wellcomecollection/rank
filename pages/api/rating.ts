import { NextApiRequest, NextApiResponse } from "next";

type Rating = {
  username: string | undefined;
  workId: string;
  query: string;
  rating: number;
  position: number;
};

export default async (req: NextApiRequest, res: NextApiResponse) => {
  if (req.method === "POST") {
    const {
      body: { username, workId, query, rating, position },
    } = req;

    if (
      // This is crap, but 0 is a valid value, but falsy in JS land
      [workId, query, rating, position].every(
        (val) => typeof val !== "undefined"
      )
    ) {
      const {
        ES_RATINGS_USER,
        ES_RATINGS_PASSWORD,
        ES_RATINGS_URL,
      } = process.env;
      const ratingDoc: Rating = {
        username,
        workId,
        query,
        rating: parseInt(rating, 10),
        position: parseInt(position, 10),
      };
      const rankEvalEnpoint = `https://${ES_RATINGS_URL}/ratings/_doc`;
      const resp = await fetch(rankEvalEnpoint, {
        method: "POST",
        body: JSON.stringify(ratingDoc),
        headers: {
          Authorization: `Basic ${Buffer.from(
            `${ES_RATINGS_USER}:${ES_RATINGS_PASSWORD}`
          ).toString("base64")}`,
          "Content-Type": "application/json",
        },
      });
      const json = await resp.json();

      if (!json.status) {
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(ratingDoc));
      } else {
        res.statusCode = json.status;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(json));
      }
    } else {
      res.statusCode = 400;
      res.setHeader("Content-Type", "application/json");
      res.end(
        JSON.stringify({
          message: "Bad Request",
          body: req.body,
          params: { username, workId, query, rating, position },
        })
      );
    }
  } else {
    res.statusCode = 405;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ message: "Method Not Allowed" }));
  }
};

export type { Rating };
