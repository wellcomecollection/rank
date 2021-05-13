import { TemplateSource } from '../../services/search-templates'
import { Rating } from '../../types'

const filterExamples = (rating: Rating, template: TemplateSource) => {
  // To avoid running exceptionally long recall queries for our negative
  // examples, we intercept the template and add a filter to only include
  // results from the set of target IDs. This should have no effect on the
  // final result, as explained in the comment below.
  const targetIds = rating.examples.flatMap((x) => x.ratings)
  const augmentedTemplate = {
    source: {
      query: {
        bool: {
          must: [template.source.query],
          filter: { terms: { _id: targetIds } },
        },
      },
    },
  }

  return augmentedTemplate
}

export { filterExamples }
