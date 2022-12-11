"""Search routes in the WroclawPortal API."""
from flask_restful import Resource, fields, marshal_with
from flask import Response, request
from flask.json import jsonify

from src.uni.dao.uni_dao import UniDao
from src.uni.dao.course_dao import CourseDao
from src.uni.dao.language_dao import CourseLanguageDao
from src.uni.dao.level_dao import CourseLevelDao
from src.uni.dao.title_dao import CourseTitleDao
from src.uni.dao.form_dao import CourseFormDao

# from flask_jwt_extended import jwt_required


class SearchUniApi(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument(
    #    "price", type=float, required=True, help="This field cannot be left blank!"
    # )
    response_fields = {
        "course_id": fields.Integer,
        "course_name": fields.String,
        "course_level_name": fields.String,
        # "level_name": fields.String,
        "discipline_name": fields.String,
        "main_discipline": fields.String,
        # "uni_id": fields.Integer,
        "uni_uid": fields.String,
        "uni_name": fields.String,
        "city": fields.String,
        "street": fields.String,
        "building": fields.String,
        "postal_code": fields.String,
        "uni_email": fields.String,
        "phone_number": fields.String,
        "www": fields.String,
    }

    @marshal_with(response_fields)
    def get(self):
        # def get_unis_filtered_from_query_string(self):
        """
        Get a single study with a unique ID.
        :param study_id: The unique identifier for a study.
        :return: A response object for the GET API request.
        """
        error = None
        query = request.args
        if query and query != "":
            print("query from request")
            print(query)
        else:
            # ?? or return all without filtering
            error = "Empty query string."

        result = UniDao.filter_unis(query)
        return result

        def post(self):
            return {}

        def put(self):
            return {}

        def delete(self):
            return None, 204


class SearchCourseApi(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument(
    #    "price", type=float, required=True, help="This field cannot be left blank!"
    # )
    response_fields = {
        "course_id": fields.Integer,
        "course_name": fields.String,
        "level": fields.String,
        "title": fields.String,
        "form": fields.String,
        "language": fields.String,
        "semesters_number": fields.Integer,
        "ects": fields.Integer,
        # "discipline_name": fields.String,
        "main_discipline": fields.String,
        # "city": fields.String,
    }

    @marshal_with(response_fields)
    def get(self):
        # def get_unis_filtered_from_query_string(self):
        """
        Get a single study with a unique ID.
        :param study_id: The unique identifier for a study.
        :return: A response object for the GET API request.
        """
        error = None
        query = request.args
        if query and query != "":
            print("args.............................")
            print(query)
        else:
            error = "Empty query string."

        result = CourseDao.filter_courses(query)

        print("result courses in route/////////////////////")
        print(result)
        for course in result:
            print(course)
            print(type(course))
            print(course.language)
            language = CourseLanguageDao.get_language_by_id(course.language)
            level = CourseLevelDao.get_level_by_id(course.level)
            form = CourseFormDao.get_form_by_id(course.form)
            title = CourseTitleDao.get_title_by_id(course.title)

            course.language = language.course_language_name
            course.form = form.course_form_name
            course.title = title.course_title_name
            course.level = level.course_level_name

            print(course)

        return result
