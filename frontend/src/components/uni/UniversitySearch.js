import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { Form, Button } from 'react-bootstrap';
import UnivercityContext from '../../context/uni/UnivercityContext';
import { searchUnisByFilters } from '../../context/uni/UnivercityActions';

const UniversitySearch = (props) => {
  const API_URL = process.env.REACT_APP_API_URL;

  const { dispatch, city, level, discipline, search } =
    useContext(UnivercityContext);

  const [disciplines, setDisciplines] = useState([]);
  const [levels, setLevels] = useState([]);
  const [cities, setCities] = useState([]);

  useEffect(() => {
    const fetchDisciplines = async () => {
      const { data } = await axios.get(`${API_URL}/uni/disciplines`);

      setDisciplines(data.disciplines);
    };

    const fetchLevels = async () => {
      const { data } = await axios.get(`${API_URL}/uni/levels`);
      setLevels(data.levels);
    };

    const fetchCities = async () => {
      const { data } = await axios.get(`${API_URL}/uni/unis/cities`);
      setCities(data.cities);
    };

    fetchDisciplines();
    fetchLevels();
    fetchCities();
  }, []);

  const handleChange = (name) => (event) => {
    dispatch({
      type: 'SET_' + name.toUpperCase() + '_FILTER',
      payload: event.target.value,
    });
  };

  const handleSearch = async (e) => {
    e.preventDefault();

    dispatch({ type: 'SET_LOADING' });

    const searchResults = await searchUnisByFilters(
      discipline,
      level,
      city,
      search
    );

    if (!Array.isArray(searchResults)) {
      console.log(
        'From Univercity after search: Not an array There was an error loading your data!'
      );
    }

    dispatch({ type: 'SEARCH_UNIS_BY_FILTERS', payload: searchResults });

    //setUniSearchWord('');
  };

  const enterKey = (e) => {
    if (e.keyCode === 13) {
      e.preventDefault();
      handleSearch();
    }
  };

  return (
    <div className="col-lg-12 col-md-12 col-sm-12 col-xs-12 align-left ">
      <h2 className="mt-4">Explore study options</h2>
      <Form>
        <Form.Control
          type="text"
          //name="uniSearchWord"
          value={search}
          onChange={handleChange('word')}
          placeholder="Enter search keywords"
          className="mt-4 "
          aria-label="SearchUni"
          onKeyDown={enterKey}
        />
        <Form.Text id="orText" className="mt-1 mb-1 text-center">
          or
        </Form.Text>

        <Form.Select
          id="disciplines"
          value={discipline}
          onChange={handleChange('discipline')}
        >
          {!discipline && <option value="">Select field of study</option>}

          {disciplines &&
            disciplines.map((item) => {
              return (
                <option key={item.discipline_id} value={item.discipline_id}>
                  {item.discipline_name}
                </option>
              );
            })}
        </Form.Select>

        <Form.Select
          id="levels"
          value={level}
          onChange={handleChange('level')}
          className="mt-2"
        >
          {!level && <option value="">Select level of study</option>}

          {levels &&
            levels.map((item) => {
              return (
                <option key={item.course_level_id} value={item.course_level_id}>
                  {item.course_level_name}
                </option>
              );
            })}
        </Form.Select>

        <Form.Select
          id="cities"
          value={city}
          onChange={handleChange('city')}
          className="mt-2"
        >
          {!city && <option value="">Select city of study in Poland</option>}

          {cities &&
            cities.map((item, i) => {
              return (
                <option key={i} value={item.city}>
                  {item.city}
                </option>
              );
            })}
        </Form.Select>
        <Button
          className="mt-2 w-100"
          variant="custom"
          type="submit"
          onClick={handleSearch}
        >
          Search by filters
        </Button>
      </Form>
    </div>
  );
};

export default UniversitySearch;
