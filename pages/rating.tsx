import { NextPage } from "next";
import { useState, useEffect } from "react";
import ListItem from "../common/components/ListItem";
import { Rating } from "./api/rating";

const Rater = ({
  workId,
  position,
  query,
}: {
  username?: string;
  workId: string;
  position: number;
  query: string;
}) => {
  const [rated, setRated] = useState<boolean>(false);
  const ratings = [
    {
      rating: 0,
      label: "Irrelevant",
    },
    {
      rating: 1,
      label: "A bit relevant",
    },
    {
      rating: 2,
      label: "Relevant",
    },
    {
      rating: 3,
      label: "Highly relevant",
    },
  ];
  return (
    <form
      onSubmit={async (event) => {
        event.preventDefault();
        const rating: Rating = {
          username: undefined,
          workId: event.currentTarget.workId.value,
          query: event.currentTarget.query.value,
          rating: parseInt(event.currentTarget.rating.value, 10),
          position: parseInt(event.currentTarget.position.value, 10),
        };

        // TODO: Do this as form data, for some reason the lambda doesn't parse the data correctly.
        // const formData = new FormData(event.currentTarget);

        const resp = await fetch("/api/rating", {
          method: "POST",
          body: JSON.stringify(rating),
          headers: {
            "Content-Type": "application/json",
            // "Content-Type": "application/x-www-form-urlencoded",
          },
        });
        const json = await resp.json();

        if (resp.status === 200) {
          setRated(true);
        }
      }}
    >
      {!rated && (
        <div>
          <input type="hidden" value={workId} name="workId" />
          <input type="hidden" value={query} name="query" />
          <input type="hidden" value={position} name="position" />
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
                key={rating.rating}
                style={{
                  marginRight: "5px",
                }}
              >
                <label>
                  <input type="radio" name="rating" value={rating.rating} />
                  {rating.label}
                </label>
              </li>
            ))}
          </ul>
          <button type="submit">Rate it!</button>
        </div>
      )}
      {rated && "Thank you"}
    </form>
  );
};

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
    contributors: any[];
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
        {results.map(
          ({ id, title, workType, description, contributors }, position) => (
            <ListItem key={id}>
              <h3>
                <a href={`https://wellcomecollection.org/works/${id}`}>
                  {title}
                </a>
              </h3>
              <p>work type: {workType.label}</p>
              <p>
                contributors:{" "}
                {contributors.map((c) => `😺 ${c.agent.label}`).join(" / ")}
              </p>
              {description && <p>{description}</p>}

              <div>
                <Rater
                  workId={id}
                  query={activeContributor}
                  position={position}
                  username={null}
                />
              </div>
            </ListItem>
          )
        )}
      </ul>
    </div>
  );
};

export default Rank;
