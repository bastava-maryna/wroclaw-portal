/* eslint-disable prettier/prettier */
import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import omitBy from 'lodash/omitBy';
import isEmpty from 'lodash/isEmpty';
import { Container, Card, Col, Row } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import '../../css/index.css';
import UnivercityContext from '../../context/uni/UnivercityContext';
import CourseCard from './CourseCard';

const UniversityDetailCard = (props) => {
  const API_URL = process.env.REACT_APP_API_URL;
  const { level, discipline, search } = useContext(UnivercityContext);
  const [uni, setUni] = useState([]);
  const [courses, setCourses] = useState([]);
  const { id } = useParams();

  useEffect(() => {
    const fetchUni = async () => {
      const { data } = await axios.get(`${API_URL}/uni/unis/uid/${id}`);

      setUni(data.uni);
    };

    fetchUni();
  }, [id]);

  useEffect(() => {
    const fetchCourses = async () => {
      const params = new URLSearchParams(
        omitBy(
          {
            discipline_name: discipline,
            level: level,
            uni_uid: id,
            search: search,
          },
          isEmpty
        )
      );
      const { data } = await axios.get(
        `${API_URL}/uni/search/courses?${params}`
      );

      setCourses(data);
    };

    fetchCourses();
  }, [discipline, id, level, search]);
  return (
    <div className="col-lg-12 col-md-12 col-sm-12 col-xs-12 mt-3 mb-2 ">
      <Card border="info" className="w-100 uni-detail-card-back">
        <Card.Body>
          <Container>
            <Row className="d-flex align-items-baseline ">
              <Col>
                <Card.Title>{uni.uni_name}</Card.Title>
              </Col>
            </Row>
            <Row>
              <Card.Text>
                <strong>Institution Type:</strong> {uni.uni_kind}
              </Card.Text>
            </Row>

            <Row>
              <Card.Text>
                <strong>Address:</strong> {uni.postal_code}, {uni.city},
                {uni.street}, {uni.building}
              </Card.Text>
            </Row>
            <Row>
              <Card.Text>
                <strong>Email:</strong> {uni.uni_email}
              </Card.Text>
            </Row>
            <Row>
              <Card.Text>
                <strong>Phone:</strong> {uni.phone_number}
              </Card.Text>
            </Row>
            <Row>
              <Col className="text-align-center">
                <Card.Link href={uni.www}>Visit Website</Card.Link>
              </Col>
            </Row>
          </Container>
        </Card.Body>
      </Card>
      {courses.map((course) => (
        <CourseCard key={course.course_id} course={course} />
      ))}
    </div>
  );
};

export default UniversityDetailCard;
