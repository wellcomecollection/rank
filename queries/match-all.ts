const query = {
  bool: {
    filter: [
      {
        term: {
          type: {
            value: 'Visible',
          },
        },
      },
    ],
  },
}

export default query
