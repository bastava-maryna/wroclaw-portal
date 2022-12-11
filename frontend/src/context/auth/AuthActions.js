/* eslint-disable prettier/prettier */
import axios from 'axios';
import { errorHandler } from '../../errorHandler';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

export async function loginUser(dispatch, loginPayload) {
  /*
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(loginPayload),
    //body: loginPayload,
  };
  */

  dispatch({ type: 'REQUEST_LOGIN' });
  try {
    //let response = await axios(`${API_URL}/users/login`, requestOptions);

    let response = await axios.post(`${API_URL}/users/login`, loginPayload);

    console.log('response in actions');
    console.log(response);

    let data = await response.data;
    console.log('data in login actions');
    console.log(data);
    //if (data.user) {
    if (data.access_token) {
      dispatch({ type: 'LOGIN_SUCCESS', payload: data });
      localStorage.setItem('user', JSON.stringify(data.user));
      localStorage.setItem('access_token', JSON.stringify(data.access_token));
      //dispatch(hideModal());
      return data;
    }
  } catch (error) {
    const errorMessage = errorHandler(error);
    dispatch({ type: 'LOGIN_ERROR', error: errorMessage });
  }
}

export async function registerUser(dispatch, userData) {
  dispatch({ type: 'REGISTER_REQUEST' });

  await axios
    .post(`${API_URL}/users`, userData)
    .then((response) => {
      console.log('response from register user in actions');
      console.log(response);
      const data = response.data;
      console.log('register data in actions');
      console.log(data);

      if (data.user.user_id > 0) {
        const registered_data = {
          user_name: userData['user_name'],
          password: userData['password'],
        };

        dispatch({ type: 'REGISTER_SUCCESS' });
        dispatch(loginUser(dispatch, registered_data));

        //dispatch(hideModal());
        //return data;
      }
    })
    .catch((error) => {
      const errorMessage = errorHandler(error);
      dispatch({ type: 'REGISTER_ERROR', error: errorMessage });
    });
}

export function logout(dispatch) {
  localStorage.removeItem('user');
  localStorage.removeItem('access_token');
  dispatch({ type: 'LOGOUT' });
}

export async function editProfile(dispatch, newProfile, user_id) {
  dispatch({ type: 'REQUEST_EDIT_PROFILE' });
  if (!user_id) {
    dispatch({ type: 'EDIT_PROFILE_FAILURE' }, 'Not authenticated');
  } else {
    console.log('before try');
    try {
      let response = await axios.put(
        `${API_URL}/users/${user_id}`,
        newProfile,
        { headers: authHeader() }
      );

      let data = await response.data;

      if (data.user) {
        localStorage.setItem('user', JSON.stringify(data.user));
        dispatch({ type: 'EDIT_PROFILE_SUCCESS', payload: data });
        //return data;
      }
    } catch (error) {
      console.log('in edit function error');
      const errorMessage = errorHandler(error);

      dispatch({ type: 'EDIT_PROFILE_FAILURE', errorMessage });
    }
  }
}

export const showModal = (modalType, modalProps) => ({
  type: 'SHOW_MODAL',
  modalType,
  modalProps,
});

export const hideModal = () => ({
  type: 'HIDE_MODAL',
});

export const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem('user'));
};
export const getAccessToken = () => {
  return JSON.parse(localStorage.getItem('access_token'));
};

export const authHeader = () => {
  const user = getCurrentUser();
  const access_token = getAccessToken();
  if (user && access_token) {
    return { Authorization: 'Bearer ' + access_token };
  } else {
    return {};
  }
};
/*
export function fetchThread(dispatch, thread_id) {
  dispatch(fetchThreadRequest());

  //fetchThreadApi(thread)
  axios
    .get(`${API_URL}/forum/threads/${thread_id}/info`, {
      headers: authHeader(),
    })
    .then((response) => {
      console.log('in fetch thread action');
      console.log(response);
      dispatch(fetchThreadSuccess(response.data));
    })
    .catch((error) => {
      const errorMessage = errorHandler(error);
      dispatch(fetchThreadFailure(errorMessage));
    });
  axios
    .get(`${API_URL}/forum/threads/${thread_id}/posts`, {
      headers: authHeader(),
    })
    .then((response) => {
      console.log('in fetch thread post action');
      console.log(response);
      dispatch(fetchThreadPostSuccess(response.data));
    })
    .catch((error) => {
      const errorMessage = errorHandler(error);
      dispatch(fetchThreadFailure(errorMessage));
    });
}
*/
export const fetchThreadRequest = () => {
  return {
    type: 'FETCH_THREAD_REQUEST',
  };
};

export const fetchThreadSuccess = (thread) => {
  return {
    type: 'FETCH_THREAD_SUCCESS',
    thread,
  };
};
export const fetchThreadPostSuccess = (posts) => {
  return {
    type: 'FETCH_THREAD_POST_SUCCESS',
    posts,
  };
};

export const fetchThreadFailure = (error) => {
  return {
    type: 'FETCH_THREAD_FAILURE',
    error,
  };
};

export async function createThread(dispatch, newThread) {
  dispatch(createThreadRequest(newThread));
  console.log('new thread in actions');
  console.log(newThread);
  //await
  axios
    //.post(`${API_URL}/threads`, newThread, { headers: authHeader() })
    .post(`${API_URL}/forum/threads`, newThread)
    .then((response) => {
      console.log('response in /threads');
      console.log(response.data.thread);
      console.log(response.data.thread['thread_id']);
      dispatch(createThreadSuccess(response.data));

      // re-load topic page
      //  await axios.get(`${API_URL}/forum/topics/${newThread.topic}/threads`, newThread)
      axios
        .get(
          `${API_URL}/forum/topics/${newThread.topic}/threads`
          //, newThread, {
          //  headers: authHeader(),
          // }
        )
        .then((response) => {
          console.log('response after reload');
          console.log(response);
          dispatch(fetchTopicSuccess(response.data));
        })
        .catch((error) => {
          const errorMessage = errorHandler(error);
          dispatch(fetchTopicFailure(errorMessage));
        });
    })
    .catch((error) => {
      const errorMessage = errorHandler(error);
      dispatch(createThreadFailure(errorMessage));
    });
}

export const createThreadRequest = (newThread) => {
  return {
    type: 'CREATE_THREAD_REQUEST',
    newThread,
  };
};

export const createThreadSuccess = (newThread) => {
  return {
    type: 'CREATE_THREAD_SUCCESS',
    newThread,
  };
};

export const createThreadFailure = (error) => {
  return {
    type: 'CREATE_THREAD_FAILURE',
    error,
  };
};

export const createThreadSave = (newThread) => {
  return {
    type: 'CREATE_THREAD_SAVE',
    name: newThread.name,
    content: newThread.content,
  };
};

export async function deleteThread(dispatch, thread_id) {
  dispatch(deleteThreadRequest());

  //deleteThreadApi(id)
  axios
    .delete(`${API_URL}/forum/threads/${thread_id}`, {
      headers: authHeader(),
    })
    .then((response) => {
      console.log('in delete thread action');
      console.log(response);
      dispatch(deleteThreadSuccess());

      // re-load thread page
      //fetchThreadApi(id)
      axios
        .get(`${API_URL}/forum/threads/${thread_id}/posts`, {
          headers: authHeader(),
        })
        .then((response) => {
          console.log('in delete thread reload thread action');
          console.log(response);
          dispatch(fetchThreadSuccess(response.data));
        })
        .catch((error) => {
          const errorMessage = errorHandler(error);
          console.log('error message in delete');
          console.log(errorMessage);
          dispatch(fetchThreadFailure(errorMessage));
        });
    })
    .catch((error) => {
      const errorMessage = errorHandler(error);
      dispatch(deleteThreadFailure(errorMessage));
    });
}

export const deleteThreadRequest = () => {
  return {
    type: 'DELETE_THREAD_REQUEST',
  };
};

export const deleteThreadSuccess = () => {
  return {
    type: 'DELETE_THREAD_SUCCESS',
  };
};

export const deleteThreadFailure = (error) => {
  return {
    type: 'DELETE_THREAD_FAILURE',
    error,
  };
};

export const fetchTopicSuccess = (topic) => {
  return {
    type: 'FETCH_TOPIC_SUCCESS',
    name: topic.name,
    //slug: topic.slug,
    //description: topic.description,
    threads: topic,
  };
};

export const fetchTopicFailure = (error) => {
  return {
    type: 'FETCH_TOPIC_FAILURE',
    error,
  };
};

//----------posts
export async function createPost(dispatch, newPost) {
  dispatch(createPostRequest());

  axios
    .post(`${API_URL}/forum/posts`, newPost, {
      //headers: {
      //  'Content-Type': 'application/json',
      //},
      headers: authHeader(),
    })
    .then((response) => {
      console.log('in create post action, response');
      console.log(response.data);
      dispatch(createPostSuccess());

      // re-load thread page
      axios
        .get(`${API_URL}/forum/threads/${newPost.thread}/posts`, {
          headers: authHeader(),
        })
        .then((response) => {
          dispatch(fetchThreadSuccess(response.data));
        })
        .catch((error) => {
          const errorMessage = errorHandler(error);
          dispatch(fetchThreadFailure(errorMessage));
        });
    })
    .catch((error) => {
      const errorMessage = errorHandler(error);
      dispatch(createPostFailure(errorMessage));
    });
}

export const createPostRequest = (newPost) => {
  return {
    type: 'CREATE_POST_REQUEST',
  };
};

export const createPostSuccess = () => {
  return {
    type: 'CREATE_POST_SUCCESS',
  };
};

export const createPostFailure = (error) => {
  return {
    type: 'CREATE_POST_FAILURE',
    error,
  };
};

export async function deletePost(dispatch, post_id, thread_id) {
  dispatch(deletePostRequest(post_id));

  axios
    .delete(`${API_URL}/forum/posts/${post_id}`, {
      headers: authHeader(),
    })
    .then((response) => {
      dispatch(deletePostSuccess(post_id));

      // re-load thread page
      axios
        .get(`${API_URL}/forum/threads/${thread_id}/posts`, {
          headers: authHeader(),
        })
        .then((response) => {
          dispatch(fetchThreadSuccess(response.data));
        })
        .catch((error) => {
          const errorMessage = errorHandler(error);
          dispatch(fetchThreadFailure(errorMessage));
        });
    })
    .catch((error) => {
      const errorMessage = errorHandler(error);
      dispatch(deletePostFailure(post_id, errorMessage));
    });
}

export const deletePostRequest = (id) => {
  return {
    type: 'DELETE_POST_REQUEST',
    id,
  };
};

export const deletePostSuccess = (id) => {
  return {
    type: 'DELETE_POST_SUCCESS',
    id,
  };
};

export const deletePostFailure = (id, error) => {
  return {
    type: 'DELETE_POST_FAILURE',
    id,
    error,
  };
};
