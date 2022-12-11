/* eslint-disable prettier/prettier */
import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { Icon, Message } from 'semantic-ui-react';
import StatusMessage from '../forum/StatusMessage';
import AuthContext from '../../context/auth/AuthContext';
import './style.css';

const Protected = ({ showRegister, showLogin }) => {
  const { isAuthenticated, isLoading, error } = useContext(AuthContext);

  const statusMessage = (
    <StatusMessage
      error={error}
      errorMessage={error || 'Login Error'}
      loading={isLoading}
      loadingMessage={'Redirecting in'}
      type="modal"
    />
  );
  if (!isAuthenticated) {
    return (
      <div>
        <Message attached header="To use forum you must login or register" />
        {statusMessage}
        <Message attached="top" info>
          <Icon name="help" />
          New to this forum?&nbsp;
          <Link className="login-register" onClick={showRegister}>
            Register here
          </Link>
        </Message>
        <Message attached="top" info>
          <Icon name="help" />
          Have an account?&nbsp;
          <Link className="login-register" onClick={showLogin}>
            Login here
          </Link>
        </Message>
        &nbsp;
      </div>
    );
  } else return null;
};

export default Protected;
