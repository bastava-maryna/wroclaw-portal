"""Voivodeship routes in the WroclawPortal API.  Used for retrieving, adding, updating, and deleting voivodeships ."""
from flask_restful import Resource
from flask import Response, request
from flask.json import jsonify
from src.uni.dao.voivodeship_dao import VoivodeshipDao

from src.uni.models.voivodeship_model import Voivodeship


class VoivodeshipIdApi(Resource):
    def get(self, voiv_id):
        """
        Get a single voivodeship with a unique ID.
        :param voiv_id: The unique identifier for a voivodeship.
        :return: A response object for the GET API request.
        """
        voivodeship = VoivodeshipDao.get_voivodeship_by_id(voiv_id=voiv_id)

        if voivodeship is None:
            response = jsonify(
                {
                    "self": f"/voivodeships/{voiv_id}",
                    "voivodeship": None,
                    "error": "there is no voivodeship with this identifier",
                }
            )
            response.status_code = 400
            return response
        else:
            voivodeship_dict: dict = Voivodeship(voivodeship).__dict__

            response = jsonify(
                {
                    "self": f"/voivodeships/{voiv_id}",
                    "voivodeship": voivodeship_dict,
                }
            )

            return Response(response, mimetype="application/json", status=200)

    def put(self, voiv_id):
        """
        Update an existing voivodeship.
        :param voiv_id: The unique identifier for a voivodeship.
        :return: A response object for the PUT API request.
        """
        old_voivodeship: Voivodeship = VoivodeshipDao.get_voivodeship_by_id(
            voiv_id=voiv_id
        )

        if old_voivodeship is None:
            response = jsonify(
                {
                    "self": f"/voivodeships/{voiv_id}",
                    "updated": False,
                    "voivodeship": None,
                    "error": "there is no existing voivodeship with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        voivodeship_data: dict = request.get_json()
        new_voivodeship = Voivodeship(voivodeship_data)

        if old_voivodeship != new_voivodeship:

            is_updated = VoivodeshipDao.update_voivodeship(voivodeship=new_voivodeship)

            if is_updated:
                updated_voivodeship: Voivodeship = VoivodeshipDao.get_voivodeship_by_id(
                    voiv_id=new_voivodeship.voiv_id
                )
                updated_voivodeship_dict: dict = Voivodeship(
                    updated_voivodeship
                ).__dict__

                response = jsonify(
                    {
                        "self": f"/voivodeships/{voiv_id}",
                        "updated": True,
                        "voivodeship": updated_voivodeship_dict,
                    }
                )

                return Response(response, mimetype="application/json", status=200)
            else:
                response = jsonify(
                    {
                        "self": f"/voivodeships/{voiv_id}",
                        "updated": False,
                        "voivodeship": None,
                        "error": "the voivodeship failed to update",
                    }
                )

                return Response(response, mimetype="application/json", status=500)
        else:
            response = jsonify(
                {
                    "self": f"/voivodeships/{voiv_id}",
                    "updated": False,
                    "voivodeship": None,
                    "error": "the voivodeship submitted is equal to the existing voivodeship with the same id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

    def delete(self, voiv_id):
        """
        Delete an existing voivodeship.
        :param voiv_id: The unique identifier for a voivodeship.
        :return: A response object for the DELETE API request.
        """
        existing_voivodeship: Voivodeship = VoivodeshipDao.get_voivodeship_by_id(
            voiv_id=voiv_id
        )

        if existing_voivodeship is None:
            response = jsonify(
                {
                    "self": f"/voivodeships/{voiv_id}",
                    "deleted": False,
                    "error": "there is no existing voivodeship with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        is_deleted = VoivodeshipDao.delete_voivodeship_by_id(voiv_id=voiv_id)

        if is_deleted:
            response = jsonify(
                {
                    "self": f"/voivodeships/{voiv_id}",
                    "deleted": True,
                }
            )

            return Response(response, mimetype="application/json", status=204)
        else:
            response = jsonify(
                {
                    "self": f"/voivodeships/{voiv_id}",
                    "deleted": False,
                    "error": "failed to delete the voivodeship",
                }
            )

            return Response(response, mimetype="application/json", status=500)


class VoivodeshipsApi(Resource):
    def get(self):
        """
        Get all the voivodeships in the database.
        :return: A response object for the GET API request.
        """
        voivodeships: list = VoivodeshipDao.get_voivodeships()

        if voivodeships is None:
            response = jsonify(
                {
                    "self": "/voivodeships",
                    "voivodeships": None,
                    "error": "an unexpected error occurred retrieving voivodeships",
                }
            )

            return Response(response, mimetype="application/json", status=500)
        else:
            voiv_dicts = [Voivodeship(voiv).__dict__ for voiv in voivodeships]

            response = jsonify({"self": "/voivodeships", "voivodeships": voiv_dicts})

            return Response(response, mimetype="application/json", status=200)
