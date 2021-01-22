export type QueryType = "works" | "images"
export type Env = "prod" | "stage"

export type Example = {
    id: string
    query: string
    ratings: [{
      _id: string
      rating: number
    }]
  }
