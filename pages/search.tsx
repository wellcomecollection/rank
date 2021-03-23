import { GetServerSideProps, NextPage } from "next";
import absoluteUrl from "next-absolute-url";
import { useState } from "react";

function removeUndefinedValues(
  obj: Record<string, unknown>
): { [key: string]: any } {
  return JSON.parse(JSON.stringify(obj));
}

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

const Search: NextPage<Props> = ({ data, search }) => {
  const [query, setQuery] = useState(search.query);
  const [queryId, setQueryId] = useState(search.queryId);

  return (
    <form>
      <div>
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
        <label className="p-2 mr-10 inline-block border-2 border-purple-400 rounded-full">
          Query ID:
          <select
            className="ml-2"
            name="queryId"
            onChange={(event) => setQueryId(event.currentTarget.value)}
          >
            <option value="">default</option>
            <option value="languages" selected={queryId === "languages"}>
              languages
            </option>
          </select>
        </label>
        <button
          className="p-2 ml-3 mr-10 inline-block border-2 border-purple-400 rounded-full"
          aria-label="Search catalogue"
          type="submit"
        >
          🔎
        </button>
      </div>
      <ul>
        {data.hits.hits.map((hit) => (
          <li key={hit._id}>
            <h2 className="mt-5 text-xl border-t">{hit._source.data.title}</h2>
            <div>Score: {hit._score}</div>
            <div>
              {hit.highlight && hit.highlight["data.title"] && (
                <div>
                  <h3 className="font-bold mt-2">Title</h3>
                  <div
                    dangerouslySetInnerHTML={{
                      __html: hit.highlight["data.title"],
                    }}
                  />
                </div>
              )}
              {hit.highlight && hit.highlight["data.contributors.agent.label"] && (
                <div>
                  <h3 className="font-bold mt-2">Contributors</h3>
                  <dd
                    dangerouslySetInnerHTML={{
                      __html: hit.highlight["data.contributors.agent.label"],
                    }}
                  />
                </div>
              )}
              {hit.highlight && hit.highlight["data.subjects.concepts.label"] && (
                <div>
                  <h3 className="font-bold mt-2">Subjects</h3>
                  <div
                    dangerouslySetInnerHTML={{
                      __html: hit.highlight["data.subjects.concepts.label"],
                    }}
                  />
                </div>
              )}
              {hit.highlight && hit.highlight["data.genres.concepts.label"] && (
                <div>
                  <h3 className="font-bold mt-2">Genres</h3>
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
    </form>
  );
};

export default Search;
