import { GetServerSideProps, NextPage } from "next";
import Head from "next/head";
import absoluteUrl from "next-absolute-url";
import React, { useState } from "react";
import { QueryType } from "../types";
import { RankEvalResponse } from "./api/eval";
import { CopyToClipboard } from "react-copy-to-clipboard";
import QueryIdSelect from "../components/QueryIdSelect";
import Submit from "../components/Submit";

type Data = {
  rankings: RankEvalResponse[];
  pass: boolean;
};
type Props = {
  data: Data;
  search: {
    queryId?: string;
  };
};

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const queryId = qs.queryId ? qs.queryId.toString() : undefined;
  const { origin } = absoluteUrl(req);
  const resp = await fetch(`${origin}/api/eval?env=prod`);
  const data = await resp.json();

  return {
    props: {
      data,
      search: JSON.parse(
        JSON.stringify({
          queryId,
        })
      ),
    },
  };
};

function scoreToEmoji(score: number): string {
  return score === 1 ? "✅" : "❌";
}

export function indexToQueryType(index: string): QueryType {
  // the name of the index should indicate the queryType, eg "images-2021-01-12"
  // should result in an "images" query
  return index.split("-")[0] as QueryType;
}

type RankingComponentProps = {
  ranking: RankEvalResponse;
};
const RankingComponent = ({ ranking }: RankingComponentProps) => {
  const [showJson, setShowJson] = useState(false);
  const elasticJson = `${ranking.query.method} ${
    ranking.query.path
  }\n${JSON.stringify(JSON.parse(ranking.query.body), null, 2)}`;
  const [copied, setCopied] = useState(false);

  return (
    <div className="py-4 font-mono" key={ranking.index}>
      <h2 className="text-2xl font-bold">
        {scoreToEmoji(ranking.metric_score)} {ranking.queryId}
      </h2>
      <div className="space-x-4">
        <span>JSON</span>
        <button
          type="button"
          onClick={() => {
            setShowJson(!showJson);
          }}
        >
          👁️
        </button>
        <CopyToClipboard
          text={elasticJson}
          onCopy={() => {
            setCopied(true);
            const t = setTimeout(() => {
              setCopied(false);
              clearTimeout(t);
            }, 1000);
          }}
        >
          <button type="button">📋</button>
        </CopyToClipboard>
        {copied && <span>Copied</span>}
        <pre
          style={{
            display: showJson ? "block" : "none",
          }}
        >
          {elasticJson}
        </pre>
      </div>
      <p>
        <b>Index:</b> {ranking.index}
      </p>
      <h3>
        <b>Queries:</b>
      </h3>
      <ul>
        {Object.entries(ranking.details).map((key, i) => {
          const query = key[0];
          const score = ranking.details[query].metric_score;
          const encodedQuery = encodeURIComponent(query);
          const queryType = indexToQueryType(ranking.index);
          const searchURL = `https://wellcomecollection.org/${queryType}?query=${encodedQuery}`;
          return (
            <li key={query}>
              {scoreToEmoji(score)} <a href={searchURL}>{query}</a>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

const Index: NextPage<Props> = ({ data: { pass, rankings }, search }) => {
  return (
    <>
      <Head>
        <title>Relevancy ranking evaluation | Wellcome Collection</title>
      </Head>

      <form className="mb-5">
        <QueryIdSelect queryId={search.queryId} />
        <Submit />
      </form>

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
        <a href="https://api.wellcomecollection.org/catalogue/v2/search-templates.json">
          see the current candidate search queries here
        </a>
        .
      </p>

      {rankings.map((ranking) => (
        <RankingComponent ranking={ranking} key={ranking.queryId} />
      ))}
    </>
  );
};

export default Index;
