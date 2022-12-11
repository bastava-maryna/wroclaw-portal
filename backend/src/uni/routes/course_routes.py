"""Studies routes in the WroclawPortal API.
Used for retrieving, adding, updating, and deleting studies ."""
from flask_restful import Resource, fields, marshal_with
from flask import Response, request
from flask.json import jsonify
from src.uni.dao.course_dao import CourseDao

from src.uni.models.course_model import (
    Course,
    CourseSchema,
    course_schema,
    courses_schema,
)

resource_fields = {
    "course_id": fields.Integer,
    "course_uid": fields.String,
    "course_name": fields.String,
    "course_isced_name": fields.String,
    "level": fields.String,
    "title": fields.String,
    "form": fields.String,
    "language": fields.String,
    "semesters_number": fields.Integer,
    "ects": fields.Integer,
    "main_discipline": fields.String,
    "institution": fields.String,
}


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
            response.status_code = 400
            return response
        else:
            course_dict: dict = Course(course).__dict__

            response = jsonify(
                {
                    "self": f"/courses/{course_id}",
                    "study": course_dict,
                }
            )

            return Response(response, mimetype="application/json", status=200)

    def put(self, course_id):
        """
        Update an existing course.
        :param course_id: The unique identifier for a course.
        :return: A response object for the PUT API request.
        """
        old_course: Course = CourseDao.get_course_by_id(course_id=course_id)

        if old_course is None:
            response = jsonify(
                {
                    "self": f"/courses/{course_id}",
                    "updated": False,
                    "course": None,
                    "error": "there is no existing course with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        course_data: dict = request.get_json()
        new_course = Course(course_data)

        if old_course != new_course:

            is_updated = CourseDao.update_course(course=new_course)

            if is_updated:
                updated_course: Course = CourseDao.get_course_by_id(
                    course_id=new_course.course_id
                )
                updated_course_dict: dict = Course(updated_course).__dict__

                response = jsonify(
                    {
                        "self": f"/courses/{course_id}",
                        "updated": True,
                        "course": updated_course_dict,
                    }
                )

                return Response(response, mimetype="application/json", status=200)
            else:
                response = jsonify(
                    {
                        "self": f"/courses/{course_id}",
                        "updated": False,
                        "course": None,
                        "error": "the course failed to update",
                    }
                )

                return Response(response, mimetype="application/json", status=500)
        else:
            response = jsonify(
                {
                    "self": f"/studies/{course_id}",
                    "updated": False,
                    "course": None,
                    "error": "the course submitted is equal to the existing course with the same id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

    def delete(self, course_id):
        """
        Delete an existing course.
        :param course_id: The unique identifier for a course.
        :return: A response object for the DELETE API request.
        """
        existing_course: Course = CourseDao.get_course_by_id(course_id=course_id)

        if existing_course is None:
            response = jsonify(
                {
                    "self": f"/courses/{course_id}",
                    "deleted": False,
                    "error": "there is no existing course with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        is_deleted = CourseDao.delete_course(course_id=course_id)

        if is_deleted:
            response = jsonify(
                {
                    "self": f"/courses/{course_id}",
                    "deleted": True,
                }
            )

            return Response(response, mimetype="application/json", status=204)
        else:
            response = jsonify(
                {
                    "self": f"/courses/{course_id}",
                    "deleted": False,
                    "error": "failed to delete the course",
                }
            )

            return Response(response, mimetype="application/json", status=500)


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


class CoursesApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        """
        Get all the studies in the database.
        :return: A response object for the GET API request.
        """
        courses: list = CourseDao.get_courses()
        print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
        print(courses)
        """
        if study_disciplines is None:
            response = jsonify(
                {
                    "self": "/study_disciplines",
                    "study_disciplines": None,
                    "error": "an unexpected error occurred retrieving study_disciplines",
                }
            )
            # response.status_code = 500
            # return response
            return Response(response, mimetype="application/json", status=500)
        else:
            study_disciplines_dicts = [
                StudyDiscipline(study_disc).__dict__ for study_disc in study_disciplines
            ]

            # for voiv_dict in voiv_dicts:
            #    voiv_dict["log"] = f'/v2/logs/{comment_dict.get("log_id")}'

            response = jsonify(
                {
                    "self": "/study_disciplines",
                    "study_disciplines": study_disciplines_dicts,
                }
            )
            # response.status_code = 200
            # return response
            return Response(response, mimetype="application/json", status=200)
        """
        res = courses_schema.dump(courses)
        print(res)

        return courses

    def post(self):
        """
        Create a new course.
        :return: A response object for the POST API request.
        """
        course_data: dict = request.get_json()

        if course_data is None:
            response = jsonify(
                {
                    "self": "/courses",
                    "added": False,
                    "course": None,
                    "error": "the request body isn't populated",
                }
            )
            response.status_code = 400
            return response
        course_to_add = Course(course_data)

        course_added_successfully: bool = CourseDao.add_course(new_course=course_to_add)

        if course_added_successfully:
            course_added = CourseDao.get_course_by_id(course_to_add.course_id)
            course_added_dict: dict = Course(course_added).__dict__

            response = jsonify(
                {
                    "self": "/courses",
                    "added": True,
                    "course": course_added_dict,
                }
            )
            response.status_code = 200
            return response
        else:
            response = jsonify(
                {
                    "self": "/courses",
                    "added": False,
                    "course": None,
                    "error": "failed to create a new course",
                }
            )
            response.status_code = 500
            return response
