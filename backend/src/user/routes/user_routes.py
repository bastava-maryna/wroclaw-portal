"""Users in the WroclawPortal API.
Used for retrieving, adding, updating, and deleting users ."""
from flask_restful import Resource
from flask import Response, request, json
from flask.json import jsonify
from src.user.dao.user_dao import UserDao
from src.utils.helpers import generate_hash, verify_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from src.user.user_model import (
    User,
    user_schema,
    users_schema,
)
from src.user.responses import response_with
from src.user import code_constants as code


class UserIdApi(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        Get a single user with a unique ID.
        :param user_id: The unique identifier for a user.
        :return: A response object for the GET API request.
        """
        user = UserDao.get_user_by_id(user_id=user_id)

        if user is None:
            return response_with(
                code.SERVER_ERROR_404, message="there is no user with this identifier"
            )
            # or
            # return Response(mimetype="application/json", status=404)
        else:
            user_dumped = user_schema.dump(user)

            res = json.dumps({"user": user_dumped})

            return response_with(code.SUCCESS_200, value={"user": user_dumped})
            # or
            # return Response(response=res, mimetype="application/json", status=200)

    @jwt_required()
    def put(self, user_id):
        """
        Update an existing user.
        :param user_id: The unique identifier for a user.
        :return: A response object for the PUT API request.
        """
        old_user: User = UserDao.get_user_by_id(user_id)

        if old_user is None:
            # message or error
            return response_with(
                code.SERVER_ERROR_404, message="there is no user with this identifier"
            )
            # or
            # return Response(mimetype="application/json", status=404)

        user_data: dict = request.get_json()

        user_data["user_id"] = user_id
        user_data["password"] = generate_hash(user_data["password"])

        new_user = User(user_data)
        new_user.user_id = user_id

        if old_user != new_user:
            is_updated = UserDao.update_user(user=new_user)

            if is_updated:
                updated_user: User = UserDao.get_user_by_id(new_user.user_id)

                updated_user_dumped = user_schema.dump(updated_user)

                res = json.dumps({"user": updated_user_dumped})

                return response_with(
                    code.SUCCESS_200, value={"user": updated_user_dumped}
                )
                # or
                # return Response(response=res, mimetype="application/json", status=200)
            else:
                return response_with(
                    code.SERVER_ERROR_500, error="the user failed to update"
                )
                # or
                # return Response({"error": "the user failed to update"},
                # mimetype="application/json", status=500)
        else:
            return response_with(
                code.BAD_REQUEST_400,
                error="the user is equal to the existing user with the same id",
            )
            # return Response(response, mimetype="application/json", status=400)

    @jwt_required()
    def delete(self, user_id):
        """
        Delete an existing user.
        :param user_id: The unique identifier for a user.
        :return: A response object for the DELETE API request.
        """
        existing_user: User = UserDao.get_user_by_id(user_id=user_id)

        if existing_user is None:
            return response_with(
                code.SERVER_ERROR_404, message="there is no user with this identifier"
            )
            # return Response(response, mimetype="application/json", status=400)

        is_deleted = UserDao.delete_user_by_id(user_id=user_id)

        if is_deleted:
            return response_with(
                code.SUCCESS_204, message="user deleted", value={"user_id": user_id}
            )
            # return Response(response, mimetype="application/json", status=204)
        else:
            return response_with(
                code.SERVER_ERROR_500, error="failed to delete the user"
            )
            # return Response(response, mimetype="application/json", status=500)


class UsersApi(Resource):
    '''
    @jwt_required()
    def get(self):
        """
        Get all the users in the database.
        :return: A response object for the GET API request.
        """
        users: list = UserDao.get_users()

        users_dumped = users_schema.dump(users)

        res = json.dumps({"users": users_dumped})

        return response_with(code.SUCCESS_200, value={"users": users_dumped})
        # or
        # return Response(response=res, mimetype="application/json", status=200)
    '''

    def post(self):
        """
        Create a new user.
        :return: A response object for the POST API request.
        """
        user_data: dict = request.get_json()

        if user_data is None:
            return response_with(
                code.BAD_REQUEST_400, error="the request body isn't populated"
            )
            # or
            # return Response(mimetype="application/json", status=400)

        if UserDao.get_user_by_user_name(user_name=user_data["user_name"]):
            return response_with(
                code.INVALID_INPUT_422,
                message="User {} already exists".format(user_data["user_name"]),
            )

        user_data["password"] = generate_hash(user_data["password"])

        user_to_add = User(user_data)

        user_added_successfully: bool = UserDao.add_user(new_user=user_to_add)

        if user_added_successfully:
            user_added = UserDao.get_user_by_id(user_to_add.user_id)

            user_dumped = user_schema.dump(user_added)

            res = json.dumps({"user": user_dumped})

            return response_with(code.SUCCESS_201, value={"user": user_dumped})
            # or
            # return Response(response=res, mimetype="application/json", status=201)

            # # response.headers.add("Access-Control-Allow-Origin", "*")

        else:
            return response_with(
                code.SERVER_ERROR_500, error="An error occured inserting the user"
            )


class UserAuthApi(Resource):
    # login user
    def post(self):
        """
        Authenticate a user by user_name.
        :return: A response object for the POST API request.
        """
        try:
            user_data: dict = request.get_json()
            print(user_data)
            if not user_data["user_name"] or not user_data["password"]:
                return response_with(
                    code.MISSING_PARAMETERS_422,
                    message="Could not verify. Login require",
                )

            user_from_db = UserDao.get_user_by_user_name(user_data["user_name"])
            print("user_from_db")
            print(user_from_db)
            if not user_from_db:
                return response_with(
                    code.UNAUTHORIZED_403,
                    message="User {} doesn't exist".format(user_data["user_name"]),
                )

            if verify_hash(user_data["password"], user_from_db.password):
                access_token = create_access_token(identity=user_data["user_name"])
                refresh_token = create_refresh_token(identity=user_data["user_name"])

                user_dumped = user_schema.dump(user_from_db)

                res = json.dumps({"user": user_dumped})

                return response_with(
                    code.SUCCESS_200,
                    value={
                        "user": user_dumped,
                        "message": "Logged in as {}".format(user_from_db.user_name),
                        "access_token": access_token,
                        #    "refresh_token": refresh_token
                    },
                )
            else:
                return response_with(code.UNAUTHORIZED_403, message="Wrong credentials")

        except Exception as e:
            print(e)
            # return "422"
            return response_with(code.SERVER_ERROR_500, error=str(e))


# "/refresh"
class UserRefreshTokenApi(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Recreate access token.
        :return: A new access token.
        """

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}
