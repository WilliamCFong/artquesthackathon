import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import configureStore from 'ArtQuestState/reducer';
import { locationReducer } from 'ArtLocations/reducer.js';


const store = configureStore({});
store.injectReducer('locations', locationReducer);

const rootElement = document.getElementById('app-root');
console.log("whooopp");

ReactDOM.render(
  <Provider store={store}>
    <h2>Loaded!</h2>
  </Provider>,
  rootElement
);
