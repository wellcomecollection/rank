import { Env } from '../types'

export type TemplateSource = { source: { query: unknown } }

export type Template = {
  id: string
  index: string
  template: TemplateSource // Should probably call this source
}

type TemplatesResponse = {
  templates: Template[]
}

type TemplateWithStringQuery = {
  id: string
  index: string
  query: string
}

type TemplatesWithStringQueryResponse = {
  templates: TemplateWithStringQuery[]
}

const endpoints = {
  stage:
    'https://api-stage.wellcomecollection.org/catalogue/v2/search-templates.json',
  prod: 'https://api.wellcomecollection.org/catalogue/v2/search-templates.json',
}

async function getSearchTemplates(env: Env): Promise<TemplatesResponse> {
  const res = await fetch(endpoints[env])
  const json: TemplatesWithStringQueryResponse = await res.json()

  // The query is returned as a string from the API
  const templates: Template[] = json.templates.map((template) => ({
    id: template.id,
    index: `ccr--${template.index}`,
    template: {
      source: {
        query: JSON.parse(template.query),
      },
    },
  }))
  return { templates }
}

export { getSearchTemplates }
