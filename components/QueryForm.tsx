import { useEffect, useState } from 'react'

type Props = {
  query?: string
  useTestQuery?: true
  endpoint?: string
}

const QueryForm = (props: Props) => {
  const [query, setQuery] = useState(props.query)
  const [useTestQuery, setUseTestQuery] = useState(props.useTestQuery)
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
        🧪 <span className="sr-only">Test query</span>
        <input
          type="checkbox"
          name="useTestQuery"
          value="true"
          checked={useTestQuery || false}
          onChange={(event) => {
            setUseTestQuery(event.currentTarget.checked ? true : undefined)
          }}
        />
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
