"""Disciplines routes in the WroclawPortal API.  Used for retrieving disciplines."""
from flask_restful import Resource
from flask import Response
from flask.json import jsonify
from src.uni.dao.discipline_dao import DisciplineDao
from src.user.responses import response_with
from src.user import code_constants as code

from src.uni.models.discipline_model import (
    discipline_schema,
    disciplines_schema,
)


class DisciplineIdApi(Resource):
    def get(self, discipline_id):
        """
        Get a single discipline with a unique ID.
        :param disc_id: The unique identifier for a discipline.
        :return: A response object for the GET API request.
        """
        discipline = DisciplineDao.get_discipline_by_id(discipline_id=discipline_id)
        print(discipline)
        if discipline is None:
            return response_with(
                code.SERVER_ERROR_404,
                message="there is no discipline with this identifier",
            )
        else:
            discipline_dumped = discipline_schema.dump(discipline)

            return response_with(
                code.SUCCESS_200, value={"discipline": discipline_dumped}
            )


class DisciplineNameApi(Resource):
    def get(self, discipline_name):
        "get discipline by name"

        discipline = DisciplineDao.get_discipline_by_name(
            discipline_name=discipline_name
        )

        if discipline is None:
            return response_with(
                code.SERVER_ERROR_404,
                message="there is no discipline with this name",
            )
        else:
            discipline_dumped = discipline_schema.dump(discipline)

            return response_with(
                code.SUCCESS_200, value={"discipline": discipline_dumped}
            )


class DisciplinesApi(Resource):
    # @marshal_with(resource_fields)
    def get(self):
        """
        Get all the disciplines in the database.
        :return: A response object for the GET API request.
        """
        disciplines: list = DisciplineDao.get_disciplines()

        if disciplines is None:
            response = jsonify(
                {
                    "self": "/disciplines",
                    "disciplines": None,
                    "error": "an unexpected error occurred retrieving disciplines",
                }
            )

            return Response(response, mimetype="application/json", status=500)
        else:
            disciplines_dumped = disciplines_schema.dump(disciplines)

            return response_with(
                code.SUCCESS_200, value={"disciplines": disciplines_dumped}
            )
