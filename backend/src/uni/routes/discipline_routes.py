"""Voivodeship routes in the WroclawPortal API.  Used for retrieving, adding, updating, and deleting voivodeships ."""
from flask_restful import Resource, fields, marshal_with
from flask import Response, request
from flask.json import jsonify
from src.uni.dao.discipline_dao import DisciplineDao

from src.uni.models.discipline_model import (
    Discipline,
    DisciplineSchema,
    discipline_schema,
    disciplines_schema,
)

resource_fields = {"discipline_id": fields.String, "discipline_name": fields.String}


class DisciplineIdApi(Resource):
    def get(self, disc_id):
        """
        Get a single discipline with a unique ID.
        :param disc_id: The unique identifier for a discipline.
        :return: A response object for the GET API request.
        """
        discipline = DisciplineDao.get_discipline_by_id(disc_id=disc_id)

        if discipline is None:
            response = jsonify(
                {
                    "self": f"/disciplines/{disc_id}",
                    "discipline": None,
                    "error": "there is no discipline with this identifier",
                }
            )
            response.status_code = 400
            return response
        else:
            discipline_dict: dict = Discipline(discipline).__dict__

            response = jsonify(
                {
                    "self": f"/disciplines/{disc_id}",
                    "discipline": discipline_dict,
                }
            )

            return Response(response, mimetype="application/json", status=200)

    def put(self, disc_id):
        """
        Update an existing discipline.
        :param disc_id: The unique identifier for a discipline.
        :return: A response object for the PUT API request.
        """
        old_discipline: Discipline = DisciplineDao.get_discipline_by_id(disc_id=disc_id)

        if old_discipline is None:
            response = jsonify(
                {
                    "self": f"/disciplines/{disc_id}",
                    "updated": False,
                    "discipline": None,
                    "error": "there is no existing discipline with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        discipline_data: dict = request.get_json()
        new_discipline = Discipline(discipline_data)

        if old_discipline != new_discipline:

            is_updated = DisciplineDao.update_discipline(discipline=new_discipline)

            if is_updated:
                updated_discipline: Discipline = DisciplineDao.get_discipline_by_id(
                    disc_id=new_discipline.discipline_id
                )
                updated_discipline_dict: dict = Discipline(updated_discipline).__dict__

                response = jsonify(
                    {
                        "self": f"/disciplines/{disc_id}",
                        "updated": True,
                        "discipline": updated_discipline_dict,
                    }
                )

                return Response(response, mimetype="application/json", status=200)
            else:
                response = jsonify(
                    {
                        "self": f"/disciplines/{disc_id}",
                        "updated": False,
                        "discipline": None,
                        "error": "the discipline failed to update",
                    }
                )

                return Response(response, mimetype="application/json", status=500)
        else:
            response = jsonify(
                {
                    "self": f"/disciplines/{disc_id}",
                    "updated": False,
                    "discipline": None,
                    "error": "the discipline submitted is equal to the existing discipline with the same id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

    def delete(self, disc_id):
        """
        Delete an existing discipline.
        :param disc_id: The unique identifier for a discipline.
        :return: A response object for the DELETE API request.
        """
        existing_discipline: Discipline = DisciplineDao.get_discipline_by_id(
            disc_id=disc_id
        )

        if existing_discipline is None:
            response = jsonify(
                {
                    "self": f"/disciplines/{disc_id}",
                    "deleted": False,
                    "error": "there is no existing discipline with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        is_deleted = DisciplineDao.delete_discipline_by_id(disc_id=disc_id)

        if is_deleted:
            response = jsonify(
                {
                    "self": f"/disciplines/{disc_id}",
                    "deleted": True,
                }
            )

            return Response(response, mimetype="application/json", status=204)
        else:
            response = jsonify(
                {
                    "self": f"/disciplines/{disc_id}",
                    "deleted": False,
                    "error": "failed to delete the discipline",
                }
            )

            return Response(response, mimetype="application/json", status=500)


class DisciplineNameApi(Resource):
    def get(self, name):
        "get discipline by name"

        discipline = Discipline.objects.get(name=name).to_json()

        if discipline is None:
            response = jsonify(
                {
                    "self": f"/disciplines/name/{name}",
                    "discipline": None,
                    "error": "there is no discipline with this name",
                }
            )
            response.status_code = 404
            return response
        else:
            return Response(discipline, mimetype="application/json", status=200)


class DisciplinesApi(Resource):
    @marshal_with(resource_fields)
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
            return disciplines

            # response = jsonify({"self": "/disciplines", "disciplines": disc_dicts})
            # return Response(response, mimetype="application/json", status=200)

    def post(self):
        """
        Create a new discipline.
        :return: A response object for the POST API request.
        """
        discipline_data: dict = request.get_json()

        if discipline_data is None:
            response = jsonify(
                {
                    "self": f"/disciplines",
                    "added": False,
                    "discipline": None,
                    "error": "the request body isn't populated",
                }
            )
            response.status_code = 400
            return response
        discipline_to_add = Discipline(discipline_data)

        discipline_added_successfully: bool = DisciplineDao.add_discipline(
            new_disc=discipline_to_add
        )

        if discipline_added_successfully:
            discipline_added = DisciplineDao.get_discipline_by_id(
                discipline_to_add.voiv_id
            )
            discipline_added_dict: dict = Discipline(discipline_added).__dict__

            response = jsonify(
                {
                    "self": "/disciplines",
                    "added": True,
                    "discipline": discipline_added_dict,
                }
            )
            response.status_code = 200
            return response
        else:
            response = jsonify(
                {
                    "self": "/disciplines",
                    "added": False,
                    "discipline": None,
                    "error": "failed to create a new discipline",
                }
            )
            response.status_code = 500
            return response
