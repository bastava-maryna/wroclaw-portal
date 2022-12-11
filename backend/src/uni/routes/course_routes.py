"""Courses routes in the WroclawPortal API.
Used for retrieving courses."""
from flask_restful import Resource
from flask.json import jsonify
from src.uni.dao.course_dao import CourseDao
from src.user.responses import response_with
from src.user import code_constants as code

from src.uni.models.course_model import (
    course_schema,
    courses_schema,
)


class CourseIdApi(Resource):
    """course api based on id"""

    def get(self, course_id):
        """
        Get a single course with a unique ID.
        :param course_id: The unique identifier for a course.
        :return: A response object for the GET API request.
        """
        course = CourseDao.get_course_by_id(course_id=course_id)

        if course is None:
            response = jsonify(
                {
                    "self": f"/courses/{course_id}",
                    "course": None,
                    "error": "there is no course with this identifier",
                }
            )
            return response_with(
                code.SERVER_ERROR_404, message="there is no course with this identifier"
            )
        else:
            course_dumped = course_schema.dump(course)

            return response_with(code.SUCCESS_200, value={"course": course_dumped})


class CoursesApi(Resource):
    def get(self):
        """
        Get all the studies in the database.
        :return: A response object for the GET API request.
        """
        courses: list = CourseDao.get_courses()

        if courses is None:
            return response_with(
                code.SERVER_ERROR_500,
                message="unexpected error while retrieving courses",
            )
        else:
            courses_dumped = courses_schema.dump(courses)

            return response_with(code.SUCCESS_200, value={"courses": courses_dumped})


"""
class CourseNameApi(Resource):
    def get(self, course_name):
        "get courses by name"

        courses = CourseDao.get_courses_by_name(course_name=course_name).to_json()
        return Response(courses, mimetype="application/json", status=200)

    def put(self, course_name):

        body = request.get_json()
        CourseDao.get_courses_by_name(course_name=course_name).update(**body)
        return "", 200

    def delete(self, course_name):

        courses = CourseDao.get_courses_by_name(course_name=course_name).delete()
        return "", 200
"""
