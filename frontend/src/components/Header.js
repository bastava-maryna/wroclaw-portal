/* eslint-disable prettier/prettier */
import React from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import '../css/index.css';
import Image from 'react-bootstrap/Image';
import UserMenu from './auth/UserMenu';

const Header = ({ title }) => {
  return (
    <Navbar className="menu-back mb-3" expand="lg" style={{ maxHeight: '50px' }}>
      <Container fluid>
        <Navbar.Brand as={Link} to="#b">
          {title}
        </Navbar.Brand>

        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll">
          <Nav
            className="ms-auto"
            style={{ maxHeight: '50px' }}
            navbarScroll
          >
            <Nav.Link as={Link} to="/">
              <i className="fa-solid fa-house"></i> Home
            </Nav.Link>

            <Nav.Link as={Link} to="/news">
              <i className="fa-solid fa-square-rss"></i> News
            </Nav.Link>

            <Nav.Link as={Link} to="/uni">
              <i className="fa-solid fa-building-columns"></i> Universities
            </Nav.Link>

            <Nav.Link as={Link} to="/map">
              <i className="fa-solid fa-map-location-dot"></i> Map
            </Nav.Link>

            <Nav.Link as={Link} to="/forum">
              <i className="fa-solid fa-message"></i> Forum
            </Nav.Link>

            <Nav.Link as={Link} to="/docs">
              <i className="fa-solid fa-file-invoice"></i> Documents
            </Nav.Link>

            <Nav.Link as={Link} to="/currency">
              <i className="fa-solid fa-coins"></i> Currency
            </Nav.Link>

            <Nav.Link as={Link} to="/qa">
            <i class="fa-sharp fa-solid fa-question"></i> Q&A
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>

      <UserMenu />
    </Navbar>
  );
};

export default Header;

/*
 <Nav.Link as={Link} to="/login">
                <i className="fa-solid fa-user-graduate"></i> Sign In
              </Nav.Link>
*/
