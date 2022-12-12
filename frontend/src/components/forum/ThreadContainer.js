import React, { useEffect, useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import axios from 'axios';
import './style.css';
import Thread from './Thread';
import AuthContext from '../../context/auth/AuthContext';
import {
  authHeader,
  createPost,
  deletePost,
  deleteThread,
  //fetchThread,
} from '../../context/auth/AuthActions';

const ThreadContainer = () => {
  const API_URL = process.env.REACT_APP_API_URL;
  const { topic_id, id } = useParams();
  console.log('topic_id,thread_id');
  console.log(topic_id, id);
  const navigate = useNavigate();

  const {
    //posts,
    curThread,
    //newPostLoading,
    //newPostError,
    //newPostSuccess,
    //deletePostList,
    isDeleting,
    deleteError,
    //threads,
    dispatch,
    name,
  } = useContext(AuthContext);

  const [currentThread, setCurrentThread] = useState([]);
  const [postss, setPostss] = useState([]);

  useEffect(() => {
    dispatch({ type: 'FETCH_THREAD_REQUEST' });

    const fetchThread = async () => {
      //const { data } = await axios
      await axios
        .get(`${API_URL}/forum/threads/${id}/info`, {
          headers: authHeader(),
        })
        .then((response) => {
          if (response.data) {
            setCurrentThread(response.data);
            dispatch({ type: 'FETCH_THREAD_SUCCESS', thread: response.data });
          } else {
            setCurrentThread(null);
            dispatch({ type: 'RESET' });
            navigate(`/forum/topics/${topic_id}`);
          }
        })
        .catch((error) => {
          dispatch({ type: 'RESET' });
          navigate(`/forum/topics/${topic_id}`);
        });
    };
    fetchThread();
  }, [id, name]);
  //}, []);

  useEffect(() => {
    const fetchThreadPosts = async () => {
      const { data } = await axios.get(`${API_URL}/forum/threads/${id}/posts`, {
        headers: authHeader(),
      });

      setPostss(data);
      dispatch({ type: 'FETCH_THREAD_POST_SUCCESS', posts: data });
    };
    if (currentThread) {
      fetchThreadPosts();
    }
  }, [id, curThread, name]);

  return (
    <>
      <Button
        className="mt-3 w-40 mb-3"
        variant="custom"
        type="submit"
        //onClick={() => navigate(-1)}
        onClick={() => navigate(`/forum/topics/${topic_id}`)}
      >
        <i className="fa-solid fa-left-long"></i> &nbsp;Back to threads
      </Button>
      <Thread
        thread={currentThread}
        posts={postss}
        createPost={createPost}
        //newPostSuccess={newPostSuccess}
        //newPostLoading={newPostLoading}
        //newPostError={newPostError}
        //deletePostList={deletePostList}
        deletePost={deletePost}
        isDeleting={isDeleting}
        deleteError={deleteError}
        deleteThread={deleteThread}
      />
    </>
  );
};

export default ThreadContainer;
