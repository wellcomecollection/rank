export default [
  {
    // Contributor and title
    query: "bulloch history of bacteriology",
    ratings: ["rkcux48q"],
  },
  {
    query: "stim",
    ratings: ["e8qxq5mv"],
  },
  {
    // ensure that we return non-typoes over typoes
    // e.g. query:stimming matches:stimming > swimming
    query: "stimming",
    ratings: ["uuem7v9a"],
  },
  {
    query: "Oxford dictionary of national biography",
    ratings: ["ruedafcw"],
  },
  {
    // Example of a known title, but not the full
    // "The Piggle : an account of the psychoanalytic treatment of a little girl / by D. W. Winnicott ; edited by Ishak Ramzy."
    query: "The Piggle",
    ratings: ["vp7q52gs"],
  },
  {
    query: "Das neue Naturheilverfahren",
    ratings: ["execg22x"],
  },
  {
    query: "bills of mortality",
    ratings: ["xwtcsk93"],
  },
  {
    // Documents match this query with equal score so are occasionally returned in a different order and this fails.
    query: "Atherosclerosis : an introduction to atherosclerosis",
    ratings: ["bcwvtknn"],
  },
  {
    query: "L0033046",
    ratings: ["kmebmktz"],
  },
  {
    query: "kmebmktz",
    ratings: ["kmebmktz"],
  },
  {
    query: "gzv2hhgy",
    ratings: ["kmebmktz"],
  },
];
