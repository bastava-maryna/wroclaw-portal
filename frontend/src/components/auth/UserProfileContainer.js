/* eslint-disable prettier/prettier */
import React, { useContext } from 'react';
import AuthContext from '../../context/auth/AuthContext';
import StatusMessage from '../../components/forum/StatusMessage';
import Profile from '../../components/auth/Profile';
import './style.css';

const UserProfileContainer = () => {
  const { user, isLoading, error } = useContext(AuthContext);

  if (error || !user || isLoading) {
    return (
      <StatusMessage
        error={error || !user}
        errorClassName="userProfile-error"
        errorMessage={error}
        loading={isLoading}
        loadingMessage={`We are fetching the user profile for you`}
        type="default"
      />
    );
  }

  return <Profile user={user} />;
};

export default UserProfileContainer;
