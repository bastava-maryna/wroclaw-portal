import { createContext, useReducer } from 'react';
import authReducer from '../auth/AuthReducer';

const AuthContext = createContext();

let user = localStorage.getItem('user')
  ? JSON.parse(localStorage.getItem('user'))
  : null;
let token = localStorage.getItem('access_token')
  ? JSON.parse(localStorage.getItem('access_token'))
  : '';

export const AuthProvider = ({ children }) => {
  const initialState = {
    isAuthenticated: user ? true : false,
    user: null || user,
    isLoading: false,
    error: null,
    isEditing: false,
    editError: null,
    editSuccess: false,
    registerError: false,
    modalType: null,
    modalProps: {},
    newThreadLoading: false,
    newThreadSuccess: false,
    newThreadName: '',
    newThreadContent: '',
    newThreadId: null,
    newThreadError: null,
    newThreadShow: false,
    isDeleting: false, //about tread
    deleteError: null, //about thread
    curThread: null,
    name: null,
    posts: [],
    newPostLoading: true,
    newPostError: null,
    newPostSuccess: false,
    deletePostList: [],
    threads: null,
  };

  const [state, dispatch] = useReducer(authReducer, initialState);

  return (
    <AuthContext.Provider
      value={{
        ...state,
        dispatch,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
