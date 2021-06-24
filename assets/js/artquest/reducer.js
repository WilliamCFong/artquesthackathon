import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';

const initialState = {
  __VERSION__: '0.0.1a'
};

const staticReducers = {

};

const createReducer = (asyncReducers) => {
  return combineReducers({
    ...staticReducers,
    ...asyncReducers,
  });
};

export default function configureStore(initialState) {
  const store = createStore(
    createReducer(),
    initialState,
    applyMiddleare(thunkMiddleware)
  );
  store.asyncReducers = {}
  store.injectReducer = (key, asyncReducer) => {
    store.replaceReducer(store.asyncReducers)
  };
  return store;
};
