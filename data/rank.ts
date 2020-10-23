const rankRequests = (index: string, templateId: string) => {
  return [
    {
      id: "title_contrib_bulloch",
      template_id: templateId,
      params: {
        query: "bulloch history of bacteriology",
      },
      ratings: [
        {
          _id: "rkcux48q",
          _index: index,
          rating: 3,
        },
      ],
    },
    {
      id: "title_stim",
      template_id: templateId,
      params: {
        query: "stim",
      },
      ratings: [
        {
          _id: "e8qxq5mv",
          _index: index,
          rating: 3,
        },
      ],
    },
    {
      id: "title_odnb",
      template_id: templateId,
      params: {
        query: "Oxford dictionary of national biography",
      },
      ratings: [
        {
          _id: "ruedafcw",
          _index: index,
          rating: 3,
        },
      ],
    },
    {
      id: "title_piggle",
      template_id: templateId,
      params: {
        query: "The Piggle",
      },
      ratings: [
        {
          _id: "vp7q52gs",
          _index: index,
          rating: 3,
        },
      ],
    },
    {
      id: "title_dasneue",
      template_id: templateId,
      params: {
        query: "Das neue Naturheilverfahren",
      },
      ratings: [
        {
          _id: "execg22x",
          _index: index,
          rating: 3,
        },
      ],
    },
    {
      id: "title_bom",
      template_id: templateId,
      params: {
        query: "bills of mortality",
      },
      ratings: [
        {
          _id: "zc9qb3t9",
          _index: index,
          rating: 3,
        },
      ],
    },
    {
      id: "title_atherosclerosis",
      template_id: templateId,
      params: {
        query: "Atherosclerosis : an introduction to atherosclerosis",
      },
      ratings: [
        {
          _id: "bcwvtknn",
          _index: index,
          rating: 3,
        },
      ],
    },
  ];
};

const rankMetric = {
  precision: {
    relevant_rating_threshold: 3,
    k: 1,
  },
};

export { rankRequests, rankMetric };
