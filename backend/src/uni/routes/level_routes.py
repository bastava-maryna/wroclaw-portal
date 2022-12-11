"""Course level routes in the WroclawPortal API.  Used for retrieving levels ."""
from flask_restful import Resource
from flask import Response
from flask.json import jsonify
from src.uni.dao.level_dao import CourseLevelDao
from src.user.responses import response_with
from src.user import code_constants as code
from src.uni.models.course_level_model import (
    course_level_schema,
    course_levels_schema,
)


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

            return response_with(
                code.SERVER_ERROR_404, message="there is no level with this identifier"
            )
        else:
            level_dumped = course_level_schema.dump(level)

            return response_with(code.SUCCESS_200, value={"level": level_dumped})


class CourseLevelsApi(Resource):
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
            levels_dumped = course_levels_schema.dump(levels)

            return response_with(code.SUCCESS_200, value={"levels": levels_dumped})
