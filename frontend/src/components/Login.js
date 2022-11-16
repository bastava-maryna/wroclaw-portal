/* eslint-disable prettier/prettier */
import React, { useState } from 'react';

import Form from 'react-bootstrap/Form';

import Button from 'react-bootstrap/Button';

import SignupScreen from '../screens/SignupScreen';

import {useNavigate} from 'react-router-dom';


export default function Login() {
  const [email, setEmail] = useState('');

  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  function validateForm() {
    return email.length > 0 && password.length > 0;
  }

  function handleSubmit(event) {
    event.preventDefault();
  }

  return (
    <div className="Login">
      <Form onSubmit={handleSubmit}>
      
        <Form.Group size="lg" controlId="email">
          <Form.Label>Email</Form.Label>

          <Form.Control
           placeholder="Type your email..."
            autoFocus
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Form.Group>

        <Form.Group size="lg" controlId="password">
          <Form.Label>Password</Form.Label>

          <Form.Control
          placeholder="Type yor password..."
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>
        
        <br />

        <Button size="lg" type="submit" disabled={!validateForm()}>
          Login
        </Button>
        <span> </span>

        <Button a href="/signup" onClick={<SignupScreen />} block size="lg" type="submit">
          
          Sign Up
        </Button>
      </Form>
    </div>
  );
}
