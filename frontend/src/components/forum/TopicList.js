import React from 'react';
import { Segment } from 'semantic-ui-react';
import StatusMessage from './StatusMessage';
import TopicCard from './TopicCard';
import './style.css';

const TopicList = ({ isLoading, error, topics }) => {
  if (error || !topics || isLoading || topics.length === 0) {
    return (
      <StatusMessage
        error={error || !topics}
        errorClassName="home-error"
        errorMessage={error}
        loading={isLoading}
        loadingMessage={'We are fetching the homepage for you'}
        nothing={topics && topics.length === 0}
        nothingMessage={'No forum to display'}
        nothingClassName="home-error"
        type="default"
      />
    );
  }

  return (
    <div className="homeContainer">
      <Segment.Group className="home-list ">
        {topics.map((topic) => {
          return <TopicCard key={topic.topic_id} topic={topic} />;
        })}
      </Segment.Group>
    </div>
  );
};

export default TopicList;
