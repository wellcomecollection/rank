import rankEval from "../rank_eval.json";
import { useState } from "react";

type RankEvalResp = {
  details: any;
};

type DocProps = { _id: string; _index: string };
const Doc = (doc: DocProps) => {
  return (
    <a href={`https://wellcomecollection.org/works/${doc._id}`}>{doc._id}</a>
  );
};

const Index = () => {
  const [results, setResults] = useState<RankEvalResp | undefined>();
  return (
    <div
      style={{
        fontFamily: "sans-serif",
      }}
    >
      <h1>Ranking evaluation</h1>
      <div>
        <div>
          <ul
            style={{
              listStyle: "none",
              padding: 0,
              margin: 0,
            }}
          >
            {rankEval.requests.map((request) => (
              <li
                style={{
                  listStyle: "none",
                  padding: 0,
                  margin: "0 0 25px 0",
                  borderTop: "5px solid silver",
                }}
              >
                <h2>
                  Query: {request.params.query}
                  {results
                    ? `(${results.details[request.id].metric_score} / 1)`
                    : ""}
                </h2>
                <h3>Expected results</h3>
                <ul
                  style={{
                    listStyle: "none",
                    padding: 0,
                    margin: 0,
                  }}
                >
                  {request.ratings.map((rating) => (
                    <li
                      key={rating._id}
                      style={{
                        border: "1px solid silver",
                        padding: "5px",
                        display: "inline-block",
                      }}
                    >
                      <div>
                        ID: <Doc {...rating} />
                      </div>
                      <div>Rating: {rating.rating}</div>
                      <div>
                        Status:{" "}
                        {!results
                          ? "Test not run"
                          : results.details[request.id].hits.find(
                              (hit) => hit.hit._id === rating._id
                            )
                          ? "Found"
                          : "Not found"}
                      </div>
                    </li>
                  ))}
                </ul>
                {results !== undefined && (
                  <div>
                    <h3>Unrated docs found</h3>
                    <div>
                      {results.details[request.id].unrated_docs.map(
                        (doc: DocProps) => (
                          <div
                            style={{
                              border: "1px solid silver",
                              padding: "5px",
                              display: "inline-block",
                            }}
                          >
                            <Doc {...doc} />
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}
              </li>
            ))}
          </ul>
          <button
            type="button"
            onClick={async () => {
              const resp = await fetch("./api/rank");
              const json: RankEvalResp = await resp.json();
              setResults(json);
            }}
          >
            Run tests {results ? " again" : ""}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Index;
