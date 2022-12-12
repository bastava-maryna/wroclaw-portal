import React, { useState, useEffect } from 'react';
import TopicList from '../components/forum/TopicList';
import { Header } from 'semantic-ui-react';
import axios from 'axios';
import '../css/index.css';

const ForumScreen = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [topics, setTopics] = useState(null);
  useEffect(() => {
    const fetchTopics = async () => {
      const { data } = await axios.get(
        'http://127.0.0.1:5000/forum/topics/info'
      );

      setTopics(data);
    };

    fetchTopics();
  }, []);

  return (
    <>
      <Header size="huge" color="violet" className="forum-header">
        Wroclaw Portal Topics
      </Header>
      <TopicList isLoading={isLoading} error={error} topics={topics} />
    </>
  );
};

export default ForumScreen;
