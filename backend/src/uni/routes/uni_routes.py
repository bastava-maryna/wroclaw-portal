"""Universities routes in the WroclawPortal API.
Used for retrieving universities."""
from flask_restful import Resource
from flask.json import jsonify
from flask import Response
from src.uni.dao.uni_dao import UniDao
from src.uni.dao.kind_dao import UniKindDao
from src.user.responses import response_with
from src.user import code_constants as code
from src.uni.models.uni_model import (
    uni_schema,
    unis_schema,
    cities_schema,
)


class UniIdApi(Resource):
    def get(self, uni_id):
        """
        Get a single uni with a unique ID.
        :param uni_id: The unique identifier for a study.
        :return: A response object for the GET API request.
        """
        uni = UniDao.get_uni_by_id(uni_id=uni_id)

        if uni is None:
            response = jsonify(
                {
                    "self": f"/unis/{uni_id}",
                    "uni": None,
                    "error": "there is no university with this identifier",
                }
            )

            return response_with(
                code.SERVER_ERROR_404,
                message="there is no university with this identifier",
            )
        else:
            uni_dumped = uni_schema.dump(uni)

            return response_with(code.SUCCESS_200, value={"uni": uni_dumped})


class UniUidApi(Resource):
    def get(self, uni_uid):
        """
        Get a single uni with a unique Uid.
        :param uni_uid: The unique identifier for a study.
        :return: A response object for the GET API request.
        """

        uni = UniDao.get_uni_by_uid(uni_uid=uni_uid)
        kind = UniKindDao.get_kind_by_id(kind_id=uni.kind)

        uni_dict = uni.__dict__
        uni_dict["uni_kind"] = kind.kind_name

        if uni is None:
            response = jsonify(
                {
                    "self": f"/unis/uid/{uni_uid}",
                    "uni": None,
                    "error": "there is no university with this identifier",
                }
            )
            return response_with(
                code.SERVER_ERROR_404,
                message="there is no university with this identifier",
            )

        else:
            uni_dumped = uni_schema.dump(uni)

            return response_with(code.SUCCESS_200, value={"uni": uni_dumped})


class UnisApi(Resource):
    def get(self):
        """
        Get all the universities in the database.
        :return: A response object for the GET API request.
        """
        unis: list = UniDao.get_unis()

        if unis is None:
            return response_with(
                code.SERVER_ERROR_500,
                message="unexpected error while retrieving universities",
            )
        else:
            unis_dumped = unis_schema.dump(unis)

            return response_with(code.SUCCESS_200, value={"unis": unis_dumped})


class CitiesApi(Resource):
    def get(self):
        """
        Get all the cities of unis in the database.
        :return: A response object for the GET API request.
        """
        cities: list = UniDao.get_cities()
        if cities is None:
            return response_with(
                code.SERVER_ERROR_500,
                message="unexpected error while retrieving cities",
            )
        else:
            cities_dumped = cities_schema.dump(cities)

            return response_with(code.SUCCESS_200, value={"cities": cities_dumped})
