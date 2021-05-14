import { FunctionComponent, useState } from 'react'
import { GetServerSideProps, NextPage } from 'next'

import Link from 'next/link'
import QueryForm from '../components/QueryForm'
import absoluteUrl from 'next-absolute-url'
import { Pass } from '../data/ratings/pass'

type Props = {
  data?: any
  search: {
    query?: string
    useTestQuery?: true
    endpoint?: string
  }
}

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const query = qs.query ? qs.query.toString() : undefined
  const useTestQuery =
    qs.useTestQuery && qs.useTestQuery === 'true' ? true : undefined
  const endpoint = qs.endpoint ? qs.endpoint.toString() : 'works'
  const { origin } = absoluteUrl(req)
  const reqQs = Object.entries({ query, useTestQuery, endpoint })
    .filter(([, v]) => Boolean(v))
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')

  const resp = await fetch(`${origin}/api/search?${reqQs}`)
  const data = await resp.json()

  return {
    props: {
      data,
      search: JSON.parse(
        JSON.stringify({
          query,
          useTestQuery,
          endpoint,
        })
      ),
    },
  }
}

type RankEvalStatusProps = {
  pass: Pass
}
const RankEvalStatus: FunctionComponent<RankEvalStatusProps> = ({ pass }) => {
  return (
    <div
      className={`w-5 h-5 mr-2 rounded-full bg-${
        pass.score === 1 ? 'green' : 'red'
      }-200`}
    >
      <span className="sr-only">{pass.score === 1 ? 'pass' : 'fail'}</span>
    </div>
  )
}

type Endpoint = 'images' | 'works'
type HitProps = { hit: any; endpoint: Endpoint }
const Hit: FunctionComponent<HitProps> = ({ hit, endpoint }) => {
  const [showExplanation, setShowExplanation] = useState(false)
  const title =
    endpoint === 'images'
      ? hit._source.source.canonicalWork.data.title
      : hit._source.data.title
  return (
    <>
      <h2 className="mt-5 text-xl border-t-4">{title}</h2>
      <div onClick={() => setShowExplanation(!showExplanation)}>
        Score: {hit._score}
      </div>
      {showExplanation && (
        <pre>{JSON.stringify(hit._explanation, null, 2)}</pre>
      )}
      {hit.highlight && (
        <>
          <h3 className="text-lg font-bold mt-2">Matches</h3>
          {hit.matched_queries && (
            <div>Queries: {hit.matched_queries.join(', ')}</div>
          )}
          <div>
            {Object.entries(hit.highlight).map(([key, highlight]) => {
              return (
                <div key={key}>
                  <h3 className="font-bold">{key}</h3>
                  {(highlight as any[]).map((text) => (
                    <div
                      key={key}
                      dangerouslySetInnerHTML={{
                        __html: text,
                      }}
                    />
                  ))}
                </div>
              )
            })}
          </div>
        </>
      )}
    </>
  )
}

const RankEval = ({ rankEval, search }) => {
  const [showRankEval, setShowRankEval] = useState(true)

  return (
    <div className="mt-5">
      <button
        type="button"
        className={`flex flex-auto items-center mr-2 mb-2 p-2 bg-indigo-${
          showRankEval ? '100' : '200'
        } rounded-full`}
        onClick={() => setShowRankEval(!showRankEval)}
      >
        <RankEvalStatus pass={rankEval.pass} />
        {rankEval.queryId}
      </button>
      {showRankEval && (
        <div className="flex flex-wrap">
          {Object.entries(rankEval.details).map(([title], i) => (
            <Link
              href={{
                pathname: '/search',
                query: JSON.parse(
                  JSON.stringify({
                    query: title,
                    queryId: search.queryId,
                    endpoint: search.endpoint,
                  })
                ),
              }}
              key={i}
            >
              <a className="flex flex-auto items-center mr-2 mb-2 p-2 bg-indigo-200 rounded-full">
                <RankEvalStatus pass={rankEval.passes[title]} />
                <div>{title}</div>
              </a>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

const Search: NextPage<Props> = ({ data, search }) => {
  return (
    <>
      <QueryForm
        query={search.query}
        useTestQuery={search.useTestQuery}
        endpoint={search.endpoint}
      />

      <h1 className="text-4xl font-bold">Tests</h1>
      {data.rankEval.map((rankEval, i) => (
        <RankEval key={i} rankEval={rankEval} search={search} />
      ))}
      <h1 className="text-4xl font-bold">Hits</h1>
      <ul>
        {data.hits.hits.map((hit) => (
          <li key={hit._id}>
            <Hit hit={hit} endpoint={search.endpoint as Endpoint} />
          </li>
        ))}
      </ul>
    </>
  )
}

export default Search
