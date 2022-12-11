/* eslint-disable prettier/prettier */
import React, { useEffect, useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import axios from 'axios';
import TopicThreadList from './TopicThreadList';
import NewThread from './NewThread';
import AuthContext from '../../context/auth/AuthContext';
import './style.css';

import {
  createThreadSave,
  //fetchTopic,
  createThread,
} from '../../context/auth/AuthActions';

const TopicContainer = () => {
  const API_URL = process.env.REACT_APP_API_URL;
  const { topic_id } = useParams();
  console.log(topic_id);

  const navigate = useNavigate();
  const {
    dispatch,
    isAuthenticated,
    newThreadShow,
    newThreadError,
    newThreadId,
    newThreadName,
    newThreadContent,
    newThreadLoading,
    newThreadSuccess,
    user,
    //threads,
    isLoading,
    error,
  } = useContext(AuthContext);

  const [threadss, setThreadss] = useState(null);
  const [topic, setTopic] = useState(null);

  useEffect(() => {
    const fetchTopic = async () => {
      const { data } = await axios.get(`${API_URL}/forum/topics/${topic_id}`);

      setTopic(data);
    };

    fetchTopic();
  }, [topic_id]);

  useEffect(() => {
    const fetchThreads = async () => {
      const { data } = await axios.get(
        `${API_URL}/forum/topics/${topic_id}/threads`
      );

      setThreadss(data);
    };

    fetchThreads();
  }, [topic_id, newThreadId]);

  const createThreadToggle = () => {
    dispatch({ type: 'CREATE_THREAD_TOGGLE' });
  };
  return (
    <div>
      <NewThread
        topic={topic_id}
        isAuthenticated={isAuthenticated}
        isLoading={newThreadLoading}
        success={newThreadSuccess}
        thread_name={newThreadName}
        thread_content={newThreadContent}
        id={newThreadId}
        error={newThreadError}
        showEditor={newThreadShow}
        createThread={createThread}
        updateNewThread={createThreadSave}
        toggleShowEditor={createThreadToggle}
        maxLength={2000}
        user={user}
        dispatch={dispatch}
      />
      <Button
        className="mt-3 w-40 mb-3"
        variant="custom"
        type="submit"
        //onClick={() => navigate(-1)}
        onClick={() => navigate('/forum')}
      >
        <i className="fa-solid fa-left-long"></i> &nbsp;Back to topics
      </Button>
      <TopicThreadList
        isLoading={isLoading}
        threads={threadss}
        error={error}
        topic={topic}
      />
    </div>
  );
};

export default TopicContainer;
