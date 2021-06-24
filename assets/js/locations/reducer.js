import { LOAD_LOCATIONS } from './actions.js';

const initialState = {
  locations: []
};

export const locationReducer = (state = initialState, action) => {
  const newState = Object.assign(
    {}, state
  );
  switch(action.type) {
    case LOAD_LOCATIONS:
      newState.locations = action.locations;
      break;
  };
};
