# Docs

How maat is built:

- [next.js](https://nextjs.org/) for building and structuring the content
- [vercel](https://vercel.com/docs/cli) and the main branch of this github repo for deployment
- [tailwind css](https://tailwindcss.com/) for styling the content
- [elasticsearch](https://www.elastic.co/) for storing the catalogue data and running queries
- [elasticsearch's rank_eval API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-rank-eval.html) for measuring performance on known results

## What it looks like

![diagram](diagram.png)

1. client sends a request to maat
2. maat gets the current search template(s) from api.wellcomecollection.org
3. maat sends a rank_eval request to the catalogue elasticsearch index using the search templates and the known examples of search-term/result pairs
4. depending on the results from rank eval, maat returns an indication of success or failure to the client
