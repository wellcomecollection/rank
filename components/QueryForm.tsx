import { useEffect, useState } from 'react'

type Props = {
  query?: string
  queryId?: string
  endpoint?: string
}

const queries = {
  works: ['alternative-title-spellings', 'languages'],
  images: ['multimatcher', 'languages'],
}

const QueryForm = (props: Props) => {
  const [query, setQuery] = useState(props.query)
  const [queryId, setQueryId] = useState(props.queryId)
  const [endpoint, setEndpoint] = useState(props.endpoint)

  useEffect(() => {
    setQuery(props.query)
  }, [props.query])

  return (
    <form className="mb-5">
      <label className="p-2 mr-10 inline-block border-2 border-purple-400 rounded-full">
        Query:
        <input
          className="ml-2"
          type="text"
          name="query"
          value={query}
          onChange={(event) => setQuery(event.currentTarget.value)}
        />
      </label>
      <label className="p-2 mr-5 inline-block border-2 border-purple-400 rounded-full">
        Endpoint
        <select
          className="ml-2"
          name="endpoint"
          onChange={(event) => setEndpoint(event.currentTarget.value)}
          value={endpoint}
        >
          <option value="works">works</option>
          <option value="images">images</option>
        </select>
      </label>
      <label className="p-2 mr-5 inline-block border-2 border-purple-400 rounded-full">
        Query ID:
        <select
          className="ml-2"
          name="queryId"
          onChange={(event) => setQueryId(event.currentTarget.value)}
          value={queryId}
        >
          <option selected value="match-all">
            match-all
          </option>
          {queries[endpoint].map((q) => {
            return (
              <option key={q} value={q}>
                {q}
              </option>
            )
          })}
        </select>
      </label>
      <button
        className="p-2 ml-3 mr-5 inline-block border-2 border-purple-400 rounded-full"
        aria-label="Search catalogue"
        type="submit"
      >
        🔎
      </button>
    </form>
  )
}

export default QueryForm
