import { useState } from 'react'

type Props = {
  queryId?: string
}
const QueryIdSelect = (props: Props) => {
  const [queryId, setQueryId] = useState(props.queryId)
  return (
    <label className="p-2 mr-10 inline-block border-2 border-purple-400 rounded-full">
      Query ID:
      <select
        className="ml-2"
        name="queryId"
        onChange={(event) => setQueryId(event.currentTarget.value)}
        value={queryId}
      >
        <option value="">default</option>
        <option value="languages">languages</option>
        <option value="alternative-title-spellings">
          alternative-title-spellings
        </option>
      </select>
    </label>
  )
}

export default QueryIdSelect
