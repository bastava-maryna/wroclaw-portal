import axios from 'axios';
import omitBy from 'lodash/omitBy';
import isEmpty from 'lodash/isEmpty';

const API_URL = process.env.REACT_APP_API_URL;

// const univercity = axios.create({
//   baseURL: API_URL,
// });

export const searchUnisByFilters = async (
  discipline_name,
  level,
  city,
  search
) => {
  const params = new URLSearchParams(
    omitBy(
      {
        discipline_name: discipline_name,
        level: level,
        city: city,
        search: search,
      },
      isEmpty
    )
  );

  try {
    const response = await axios.get(`${API_URL}/uni/search/unis?${params}`);
    return response.data;
  } catch (err) {
    console.log(err);
  }
};

export const getStudyDisciplines = async (e) => {
  const response = await axios.get(`${API_URL}/uni/disciplines`);

  return response.data;
};

export const getUnis = async (e) => {
  const response = await axios.get(`${API_URL}/uni/unis`);

  return response.data;
};
