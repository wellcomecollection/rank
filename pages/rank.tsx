import { NextPage } from "next";
import { useState, useEffect } from "react";
import ListItem from "../components/ListItem";

const Rank: NextPage = () => {
  const contributors = [
    "eadweard muybridge",
    "frederic cayley robinson",
    "juno calypso",
    "lawson tait",
    "marie stopes",
    "mary bishop",
    "william blake",
  ];
  const ratings = [
    {
      rank: 0,
      label: "Irrelevant",
    },
    {
      rank: 1,
      label: "A bit relevant",
    },
    {
      rank: 2,
      label: "Relevant",
    },
    {
      rank: 3,
      label: "Highly relevant",
    },
  ];

  const [activeContributor, setActiveContributor] = useState<
    string | undefined
  >();

  type WorkType = {
    id: string;
    label: string;
  };
  type Result = {
    id: string;
    title: string;
    workType: WorkType;
    description: string | null;
  };
  const [results, setResults] = useState<Result[]>([]);

  async function get(query: string) {
    const resp = await fetch(`/api/search?query=${query}`);
    const json: Result[] = await resp.json();
    setResults(json);
  }
  useEffect(() => {
    if (activeContributor) {
      get(activeContributor);
    }
  }, [activeContributor]);

  return (
    <div>
      <h2>Searching for</h2>
      <ul
        style={{
          listStyle: "none",
          padding: 0,
          margin: 0,
        }}
      >
        {contributors.map((contributor) => (
          <li key={contributor}>
            <label>
              <input
                type="radio"
                name="contributor"
                value={contributor}
                onChange={(event) => {
                  setActiveContributor(event.currentTarget.value);
                }}
              />
              {contributor}
            </label>
          </li>
        ))}
      </ul>
      <ul
        style={{
          listStyle: "none",
          padding: 0,
          margin: 0,
        }}
      >
        {results.map(({ id, title, workType, description }) => (
          <ListItem key={id}>
            <a href={`https://wellcomecollection.org/works/${id}`}>
              <h3>{title}</h3>
              <p>work type: {workType.label}</p>
              {description && <p>{description}</p>}
            </a>
            <div>
              <ul
                style={{
                  display: "flex",
                  listStyle: "none",
                  padding: 0,
                  margin: 0,
                }}
              >
                {ratings.map((rating) => (
                  <li
                    style={{
                      marginRight: "5px",
                    }}
                  >
                    <label>
                      <input type="radio" name={`rating-${id}`} />
                      {rating.label}
                    </label>
                  </li>
                ))}
              </ul>
            </div>
          </ListItem>
        ))}
      </ul>
    </div>
  );
};

export default Rank;
