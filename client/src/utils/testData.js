let pingData = {
  ping: [
    {
      id: 1,
      location: [2, 2],
      active: true,
    },
    {
      id: 2,
      location: [9, 9],
      active: true,
    },
    {
      id: 3,
      location: [2, 9],
      active: true,
    },
    {
      id: 4,
      location: [9, 2],
      active: true,
    },
  ],
};

let wallData = [
  {
    vert1: [1, 1],
    vert2: [1, 10],
  },
  {
    vert1: [1, 10],
    vert2: [10, 10]
  },
  {
    vert1: [10, 10],
    vert2: [10, 1]
  },
  {
    vert1: [10, 1],
    vert2: [1, 1]
  },
];

let pipeData = [
  {
    vert1: [2, 9],
    vert2: [9, 9],
  },
  {
    vert1: [2, 2],
    vert2: [9, 2]
  },
];

export { pingData, wallData, pipeData };
