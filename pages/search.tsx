import { FunctionComponent, useEffect, useState } from "react";
import { GetServerSideProps, NextPage } from "next";
import Link from "next/link";
import absoluteUrl from "next-absolute-url";
import QueryIdSelect from "../components/QueryIdSelect";
import Submit from "../components/Submit";

type Props = {
  data?: any;
  search: {
    query?: string;
    queryId?: string;
  };
};

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const query = qs.query ? qs.query.toString() : undefined;
  const queryId = qs.queryId ? qs.queryId.toString() : undefined;
  const { origin } = absoluteUrl(req);
  const reqQs = Object.entries({ query, queryId })
    .filter(([k, v]) => Boolean(v))
    .map(([k, v]) => `${k}=${v}`)
    .join("&");

  const resp = await fetch(`${origin}/api/search/works?${reqQs}`);
  const data = await resp.json();

  return {
    props: {
      data,
      search: JSON.parse(
        JSON.stringify({
          query,
          queryId,
        })
      ),
    },
  };
};

type RankEvalStatusProps = {
  score: number;
};
const RankEvalStatus: FunctionComponent<RankEvalStatusProps> = ({ score }) => {
  return (
    <div
      className={`w-5 h-5 mr-2 rounded-full bg-${
        score === 1 ? "green" : "red"
      }-200`}
    >
      <span className="sr-only">{score === 1 ? "pass" : "fail"}</span>
    </div>
  );
};

const Search: NextPage<Props> = ({ data, search }) => {
  const [query, setQuery] = useState(search.query);
  const [showRankEval, setShowRankEval] = useState(false);
  useEffect(() => {
    setQuery(search.query);
  }, [search.query]);

  return (
    <>
      <form className="mb-5">
        <label className="p-2 mr-10 inline-block border-2 border-purple-400 rounded-full">
          Query:{" "}
          <input
            className="ml-2"
            type="text"
            name="query"
            value={query}
            onChange={(event) => setQuery(event.currentTarget.value)}
          />
        </label>
        <QueryIdSelect queryId={search.queryId} />
        <Submit />
      </form>
      <h1 className="text-4xl font-bold">Search</h1>
      <div className="mt-5">
        <button
          type="button"
          className={`flex flex-auto items-center mr-2 mb-2 p-2 bg-indigo-${
            showRankEval ? "100" : "200"
          } rounded-full`}
          onClick={() => setShowRankEval(!showRankEval)}
        >
          <RankEvalStatus
            score={
              Object.values(data.rankEval.details).every(
                (ranking) => ((ranking as any).metric_score as any) === 1
              )
                ? 1
                : 0
            }
          />
          Rank eval
        </button>
        {showRankEval && (
          <div className="flex flex-wrap">
            {Object.entries(data.rankEval.details).map(
              ([title, ranking], i) => (
                <Link
                  href={{
                    pathname: "/search",
                    query: JSON.parse(
                      JSON.stringify({
                        query: title,
                        queryId: search.queryId,
                      })
                    ),
                  }}
                  key={i}
                >
                  <a className="flex flex-auto items-center mr-2 mb-2 p-2 bg-indigo-200 rounded-full">
                    <RankEvalStatus score={(ranking as any).metric_score} />
                    <div>{title}</div>
                  </a>
                </Link>
              )
            )}
          </div>
        )}
      </div>
      <ul>
        {data.hits.hits.map((hit) => (
          <li key={hit._id}>
            <h2 className="mt-5 text-xl border-t">{hit._source.data.title}</h2>
            <div>Score: {hit._score}</div>
            <h3 className="text-lg font-bold mt-2">Matches</h3>
            <div>
              {hit.highlight && hit.highlight["data.title"] && (
                <div>
                  <h3 className="font-bold">Title</h3>
                  <div
                    dangerouslySetInnerHTML={{
                      __html: hit.highlight["data.title"],
                    }}
                  />
                </div>
              )}
              {hit.highlight && hit.highlight["data.contributors.agent.label"] && (
                <div>
                  <h3 className="font-bold">Contributors</h3>
                  <dd
                    dangerouslySetInnerHTML={{
                      __html: hit.highlight["data.contributors.agent.label"],
                    }}
                  />
                </div>
              )}
              {hit.highlight && hit.highlight["data.subjects.concepts.label"] && (
                <div>
                  <h3 className="font-bold">Subjects</h3>
                  <div
                    dangerouslySetInnerHTML={{
                      __html: hit.highlight["data.subjects.concepts.label"],
                    }}
                  />
                </div>
              )}
              {hit.highlight && hit.highlight["data.genres.concepts.label"] && (
                <div>
                  <h3 className="font-bold">Genres</h3>
                  <div
                    dangerouslySetInnerHTML={{
                      __html: hit.highlight["data.genres.concepts.label"],
                    }}
                  />
                </div>
              )}
            </div>
          </li>
        ))}
      </ul>
    </>
  );
};

export default Search;
