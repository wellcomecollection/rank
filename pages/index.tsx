import { NextPage } from "next";
import absoluteUrl from "next-absolute-url";

type Ranking = {
  queryId: string;
  metric_score: number;
  index: string;
  details: Record<string, any>;
};

type IndexProps = {
  rankings: Ranking[];
  pass: boolean;
};

function scoreToEmoji(score: number): string {
  return score === 1 ? "✅" : "❌";
}

function formatRanking(ranking: Ranking) {
  return (
    <div className="py-4 font-mono">
      <h2 className="text-2xl font-bold">
        {scoreToEmoji(ranking.metric_score)} {ranking.queryId}
      </h2>
      <p>
        <b>Index:</b> {ranking.index}
      </p>
      <h3>
        <b>Searches:</b>
      </h3>
      <ul>
        {Object.keys(ranking.details).map(function (key, i) {
          const score = ranking.details[key].metric_score;
          return (
            <li>
              {scoreToEmoji(score)} {key.toString()}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
const Index: NextPage<IndexProps> = ({ rankings, pass }) => {
  return (
    <body className="px-4 py-2 lg:max-w-3xl max-w-2xl">
      <div>
        <h1 className="text-4xl font-bold">Rank eval</h1>
        <p className="py-2">
          When someone runs a search on{" "}
          <a href="https://wellcomecollection.org/works">
            wellcomecollection.org
          </a>
          , we transform their search terms into some structured json. That json
          forms the <i>query</i> which is run against our data in elasticsearch.
          <br />
          We update the structure of our queries periodically to improve the
          relevance of our search results.
          <br />
          Every time we update a query, we test it against a set of known search
          terms, making sure that we're always showing people the right stuff.
          <br />
          You can{" "}
          <a href="https://api-stage.wellcomecollection.org/catalogue/v2/search-templates.json">
            see the current candidate search queries here
          </a>
          .
        </p>
      </div>

      <div>{rankings.map((ranking) => formatRanking(ranking))}</div>
    </body>
  );
};

Index.getInitialProps = async ({ req }): Promise<IndexProps> => {
  const { origin } = absoluteUrl(req);
  const resp = await fetch(`${origin}/api/eval?env=stage`);
  const props = await resp.json();
  return props;
};

export default Index;
