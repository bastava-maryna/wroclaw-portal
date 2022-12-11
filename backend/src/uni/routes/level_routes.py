"""Voivodeship routes in the WroclawPortal API.  Used for retrieving, adding, updating, and deleting voivodeships ."""
from flask_restful import Resource, fields, marshal_with
from flask import Response, request
from flask.json import jsonify
from src.uni.dao.level_dao import CourseLevelDao

from src.uni.models.course_level_model import (
    CourseLevel,
    CourseLevelSchema,
    course_level_schema,
    course_levels_schema,
)

resource_fields = {
    "course_level_id": fields.Integer,
    "course_level_name": fields.String,
}


class CourseLevelIdApi(Resource):
    def get(self, level_id):
        """
        Get a single level with a unique ID.
        :param level_id: The unique identifier for a level.
        :return: A response object for the GET API request.
        """
        level = CourseLevelDao.get_level_by_id(level_id=level_id)

        if level is None:
            response = jsonify(
                {
                    "self": f"/levels/{level_id}",
                    "level": None,
                    "error": "there is no level with this identifier",
                }
            )
            response.status_code = 400
            return response
        else:
            level_dict: dict = CourseLevel(level).__dict__

            response = jsonify(
                {
                    "self": f"/levels/{level_id}",
                    "level": level_dict,
                }
            )

            return Response(response, mimetype="application/json", status=200)

    def put(self, level_id):
        """
        Update an existing level.
        :param level_id: The unique identifier for a level.
        :return: A response object for the PUT API request.
        """
        old_level: CourseLevel = CourseLevelDao.get_level_by_id(level_id=level_id)

        if old_level is None:
            response = jsonify(
                {
                    "self": f"/levels/{level_id}",
                    "updated": False,
                    "level": None,
                    "error": "there is no existing level with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        level_data: dict = request.get_json()
        new_level = CourseLevel(level_data)

        if old_level != new_level:

            is_updated = CourseLevelDao.update_level(level=new_level)

            if is_updated:
                updated_level: CourseLevel = CourseLevelDao.get_level_by_id(
                    level_id=new_level.course_level_id
                )
                updated_level_dict: dict = CourseLevel(updated_level).__dict__

                response = jsonify(
                    {
                        "self": f"/levels/{level_id}",
                        "updated": True,
                        "level": updated_level_dict,
                    }
                )

                return Response(response, mimetype="application/json", status=200)
            else:
                response = jsonify(
                    {
                        "self": f"/levels/{level_id}",
                        "updated": False,
                        "level": None,
                        "error": "the level failed to update",
                    }
                )

                return Response(response, mimetype="application/json", status=500)
        else:
            response = jsonify(
                {
                    "self": f"/levels/{level_id}",
                    "updated": False,
                    "level": None,
                    "error": "the level submitted is equal to the existing level with the same id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

    def delete(self, level_id):
        """
        Delete an existing level.
        :param level_id: The unique identifier for a level.
        :return: A response object for the DELETE API request.
        """
        existing_level: CourseLevel = CourseLevelDao.get_level_by_id(level_id=level_id)

        if existing_level is None:
            response = jsonify(
                {
                    "self": f"/levels/{level_id}",
                    "deleted": False,
                    "error": "there is no existing level with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        is_deleted = CourseLevelDao.delete_level_by_id(level_id=level_id)

        if is_deleted:
            response = jsonify(
                {
                    "self": f"/levels/{level_id}",
                    "deleted": True,
                }
            )

            return Response(response, mimetype="application/json", status=204)
        else:
            response = jsonify(
                {
                    "self": f"/levels/{level_id}",
                    "deleted": False,
                    "error": "failed to delete the levele",
                }
            )

            return Response(response, mimetype="application/json", status=500)


class CourseLevelNameApi(Resource):
    def get(self, name):
        "get level by name"

        level = CourseLevel.objects.get(name=name).to_json()
        if level is None:
            response = jsonify(
                {
                    "self": f"/levels/name/{name}",
                    "discipline": None,
                    "error": "there is no level with this name",
                }
            )
            response.status_code = 404
            return response
        else:
            return Response(level, mimetype="application/json", status=200)


class CourseLevelsApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        """
        Get all the levels in the database.
        :return: A response object for the GET API request.
        """
        levels: list = CourseLevelDao.get_levels()

        if levels is None:
            response = jsonify(
                {
                    "self": "/levels",
                    "levels": None,
                    "error": "an unexpected error occurred retrieving levels",
                }
            )

            return Response(response, mimetype="application/json", status=500)
        else:
            return levels

            # response = jsonify({"self": "/levels", "levels": level_dicts})
            # return Response(response, mimetype="application/json", status=200)

    def post(self):
        """
        Create a new level.
        :return: A response object for the POST API request.
        """
        level_data: dict = request.get_json()

        if level_data is None:
            response = jsonify(
                {
                    "self": f"/levels",
                    "added": False,
                    "level": None,
                    "error": "the request body isn't populated",
                }
            )
            response.status_code = 400
            return response
        if CourseLevelDao.get_level_by_name(level_name=level_data["level_name"]):
            return Response(
                {
                    "message": "A voivodeship with name '{} already exists.".format(
                        level_data["level_name"]
                    )
                },
                mimetype="application/json",
                status=400,
            )

        level_to_add = CourseLevel(level_data)

        level_added_successfully: bool = CourseLevelDao.add_level(
            new_level=level_to_add
        )

        if level_added_successfully:
            level_added = CourseLevelDao.get_level_by_id(level_to_add.course_level_id)
            level_added_dict: dict = CourseLevel(level_added).__dict__

            response = jsonify(
                {
                    "self": "/levels",
                    "added": True,
                    "level": level_added_dict,
                }
            )
            response.status_code = 200
            return response
        else:
            response = jsonify(
                {
                    "self": "/levels",
                    "added": False,
                    "levele": None,
                    "error": "failed to create a new level",
                }
            )
            response.status_code = 500
            return response
