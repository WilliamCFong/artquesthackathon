import fetch from 'cross-fetch';

export const LOAD_LOCATIONS = 'LOAD_LOCATIONS';


export const fetchAllLocations = () => {
  const url = '/api/art/locations/';

  return (dispatch) => {
    return fetch(url)
      .then(
        (response) => response.json(),
        (error) => console.log('An error occured: ', error)
      )
      .then(
        (json) => dispatch(loadLocations(json))
      );
  };
};


export const loadLocations = (json) => {
  return {
    type: LOAD_LOCATIONS,
    locations: json,
  };
};
