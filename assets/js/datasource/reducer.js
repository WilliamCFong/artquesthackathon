//import {} FROM './actions.js';

const initialState = {
  cityDataSource: {},
};

export const cityDataSourceReducer = (state = initialState, action) => {
  console.log(action);
  const newState = Object.assign(
    {}, state
  );
  return newState;
};
