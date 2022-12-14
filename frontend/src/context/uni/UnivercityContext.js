/* eslint-disable prettier/prettier */
import { createContext, useReducer } from 'react';
import univercityReducer from './UnivercityReducer';

const UnivercityContext = createContext();

export const UnivercityProvider = ({ children }) => {
  const initialState = {
    discipline: '',
    search: '',
    level: '',
    city: '',
    searchUniResults: [],
    loading: false,
  };

  const [state, dispatch] = useReducer(univercityReducer, initialState);

  return (
    <UnivercityContext.Provider
      value={{
        ...state,
        dispatch,
      }}
    >
      {children}
    </UnivercityContext.Provider>
  );
};

export default UnivercityContext;
