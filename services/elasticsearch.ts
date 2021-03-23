import { Client } from "@elastic/elasticsearch";

const {
  ES_USER,
  ES_PASSWORD,
  ES_CLOUD_ID,
  ES_RATINGS_USER,
  ES_RATINGS_PASSWORD,
  ES_RATINGS_CLOUD_ID,
} = process.env;

const client = new Client({
  cloud: {
    id: ES_CLOUD_ID,
  },
  auth: {
    username: ES_USER,
    password: ES_PASSWORD,
  },
});

const ratingClient = new Client({
  cloud: {
    id: ES_RATINGS_CLOUD_ID,
  },
  auth: {
    username: ES_RATINGS_USER,
    password: ES_RATINGS_PASSWORD,
  },
});

export { client, ratingClient };
