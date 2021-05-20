import { FunctionComponent, useEffect, useState } from 'react'

type Props = {
  query?: string
  useTestQuery?: true
  namespace?: string
}

const QueryForm: FunctionComponent<Props> = (props) => {
  const [query, setQuery] = useState(props.query)
  const [useTestQuery, setUseTestQuery] = useState(props.useTestQuery)
  const [namespace, setNamespace] = useState(props.namespace)

  useEffect(() => {
    setQuery(props.query)
  }, [props.query])

  return (
    <form className="mb-5 border-2 border-purple-400 rounded-full flex">
      <div className="flex-grow">
        <label className="p-2 mr-4 inline-block">
          Query
          <input
            className="ml-2"
            type="text"
            name="query"
            value={query}
            placeholder="What are you looking for?"
            onChange={(event) => setQuery(event.currentTarget.value)}
          />
        </label>
        <label className="p-2 mr-4 inline-block">
          Endpoint
          <select
            className="ml-2"
            name="endpoint"
            onChange={(event) => setNamespace(event.currentTarget.value)}
            value={namespace}
          >
            <option value="works">works</option>
            <option value="images">images</option>
          </select>
        </label>
      </div>
      <div className="flex-shrink">
        <label className="p-2 inline-block">
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
          className="p-2 ml-3"
          aria-label="Search catalogue"
          type="submit"
        >
          🔎
        </button>
      </div>
    </form>
  )
}

export default QueryForm
