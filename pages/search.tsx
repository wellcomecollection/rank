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
  };
};

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const query = qs.query ? qs.query.toString() : undefined;
  const { origin } = absoluteUrl(req);
  const resp = await fetch(
    `${origin}/api/search/works${query ? `?query=${query}` : ``}`
  );

  const data = await resp.json();

  return {
    props: {
      data,
      search: {
        query,
      },
    },
  };
};

const Search: NextPage<Props> = ({ data, search }) => {
  const [query, setQuery] = useState(search.query);
  return (
    <form>
      <div>
        <label>
          Query:{" "}
          <input
            className="border-2 border-indigo-600"
            type="text"
            name="query"
            value={query}
            onChange={(event) => setQuery(event.currentTarget.value)}
          />
        </label>
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
