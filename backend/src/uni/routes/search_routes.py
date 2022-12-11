"""Search routes in the WroclawPortal API."""
from flask_restful import Resource, fields, marshal_with
from flask import request
from flask.json import jsonify

from src.uni.dao.uni_dao import UniDao
from src.uni.dao.course_dao import CourseDao
from src.uni.dao.language_dao import CourseLanguageDao
from src.uni.dao.level_dao import CourseLevelDao
from src.uni.dao.title_dao import CourseTitleDao
from src.uni.dao.form_dao import CourseFormDao


class SearchUniApi(Resource):
    response_fields = {
        "course_id": fields.Integer,
        "course_name": fields.String,
        "course_level_name": fields.String,
        "discipline_name": fields.String,
        "main_discipline": fields.String,
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
        """
        Get courses with university info by parameters from query string.
        :param search: The search word to filter university by fields of study (like criteria).
        :param discipline_name: The discipline to filter university by fields of study.
        :param level: The level to filter university by levels.
        :param city: The city to filter university by cities.
        :return: A response object for the GET API request.
        """
        error = None
        query = request.args
        if query and query != "":
            print("query from request")
            print(query)
        else:
            # return all without filtering
            error = "Empty query string."

        result = UniDao.filter_unis(query)
        return result


class SearchCourseApi(Resource):
    response_fields = {
        "course_id": fields.Integer,
        "course_name": fields.String,
        "level": fields.String,
        "title": fields.String,
        "form": fields.String,
        "language": fields.String,
        "semesters_number": fields.Integer,
        "ects": fields.Integer,
        "main_discipline": fields.String,
    }

    @marshal_with(response_fields)
    def get(self):
        """
        Get courses info by parameters from query string.
        :param search: The search word to filter courses by fields of study (like criteria).
        :param discipline_name: The discipline to filter courses by fields of study.
        :param level: The level to filter courses by levels.
        :param uni_uid: The university to filter courses.
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

        for course in result:
            language = CourseLanguageDao.get_language_by_id(course.language)
            level = CourseLevelDao.get_level_by_id(course.level)
            form = CourseFormDao.get_form_by_id(course.form)
            title = CourseTitleDao.get_title_by_id(course.title)

            course.language = language.course_language_name
            course.form = form.course_form_name
            course.title = title.course_title_name
            course.level = level.course_level_name

        return result
