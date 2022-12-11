"""Posts in the WroclawPortal API.
Used for retrieving, adding, updating, and deleting posts ."""
from flask_restful import Resource, fields, marshal_with
from flask import Response, request
from flask.json import jsonify
from src.forum.dao.post_dao import PostDao
from src.forum.dao.thread_dao import ThreadDao
from src.forum.models.post_model import Post
from flask_jwt_extended import jwt_required
from src.forum.models.post_model import (
    Post,
    post_schema,
    posts_schema,
)

resource_fields = {
    "post_id": fields.Integer,
    "post_content": fields.String,
    "post_created_at": fields.String,
    "post_updated_at": fields.String,
    "post_creator": fields.Integer,
    "thread": fields.Integer,
}


class PostIdApi(Resource):
    @marshal_with(resource_fields)
    def get(self, post_id):
        """
        Get a single post with a unique ID.
        :param post_id: The unique identifier for a post.
        :return: A response object for the GET API request.
        """
        post = PostDao.get_post_by_id(post_id=post_id)
        print(type(post))
        print(post)
        return post
        """
        if thread is None:
            response = jsonify(
                {
                    "self": f"/threads/{thread_id}",
                    "thread": None,
                    # "log": None,
                    "error": "there is no thread with this identifier",
                }
            )
            response.status_code = 400
            return response
        else:
            thread_dict: dict = Thread(thread).__dict__
            # comment_dict["time"] = str(comment_dict["time"])

            response = jsonify(
                {
                    "self": f"/threads/{thread_id}",
                    "thread": thread_dict,
                    # "log": f'/v2/logs/{comment_dict.get("log_id")}',
                }
            )
            # response.status_code = 200
            # return response
            return Response(response, mimetype="application/json", status=200)
        """

    def put(self, post_id):
        """
        Update an existing post.
        :param post_id: The unique identifier for a post.
        :return: A response object for the PUT API request.
        """
        old_post: Post = PostDao.get_post_by_id(post_id=post_id)

        if old_post is None:
            response = jsonify(
                {
                    "self": f"/posts/{post_id}",
                    "updated": False,
                    "post": None,
                    "error": "there is no existing post with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        post_data: dict = request.get_json()
        new_post = Post(post_data)

        if old_post != new_post:

            is_updated = PostDao.update_post(post=new_post)

            if is_updated:
                updated_post: Post = PostDao.get_post_by_id(post_id=new_post.post_id)
                updated_post_dict: dict = Post(updated_post).__dict__

                response = jsonify(
                    {
                        "self": f"/posts/{post_id}",
                        "updated": True,
                        "post": updated_post_dict,
                    }
                )

                return Response(response, mimetype="application/json", status=200)
            else:
                response = jsonify(
                    {
                        "self": f"/posts/{post_id}",
                        "updated": False,
                        "post": None,
                        "error": "the post failed to update",
                    }
                )

                return Response(response, mimetype="application/json", status=500)
        else:
            response = jsonify(
                {
                    "self": f"/posts/{post_id}",
                    "updated": False,
                    "post": None,
                    "error": "the post submitted is equal to the existing post with the same id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

    def delete(self, post_id):
        """
        Delete an existing post.
        :param post_id: The unique identifier for a post.
        :return: A response object for the DELETE API request.
        """
        existing_post: Post = PostDao.get_post_by_id(post_id=post_id)

        if existing_post is None:
            response = jsonify(
                {
                    "self": f"/posts/{post_id}",
                    "deleted": False,
                    "error": "there is no existing post with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        is_deleted = PostDao.delete_post_by_id(post_id=post_id)

        if is_deleted:
            response = jsonify(
                {
                    "self": f"/posts/{post_id}",
                    "deleted": True,
                }
            )

            return Response(response, mimetype="application/json", status=204)
        else:
            response = jsonify(
                {
                    "self": f"/posts/{post_id}",
                    "deleted": False,
                    "error": "failed to delete the post",
                }
            )

            return Response(response, mimetype="application/json", status=500)


class PostsApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        """
        Get all the posts in the database.
        :return: A response object for the GET API request.
        """
        print("in routes///////////////////")
        posts: list = PostDao.get_posts()

        return posts
        """
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
            disc_dicts = [Discipline(disc).__dict__ for disc in disciplines]

            # for voiv_dict in voiv_dicts:
            #    voiv_dict["log"] = f'/v2/logs/{comment_dict.get("log_id")}'

            response = jsonify({"self": "/disciplines", "disciplines": disc_dicts})

            return Response(response, mimetype="application/json", status=200)
        """

    @marshal_with(resource_fields)
    def post(self):
        # if Voivodeship.objects.get(name=name):
        #    return {
        #        "message": "A voivodeship with name '{} already exists.".format(name)
        #    }, 400

        # data = Uni.parser.parse_args()

        # uni = UniModel(name, data["price"])

        # try:
        #    uni.save_to_db()
        # except:
        #    return {"message": "An error occured inserting the item"}, 500

        # return uni.json(), 201
        """
        Create a new post.
        :return: A response object for the POST API request.
        """
        post_data: dict = request.get_json()
        print("post_data from request")
        print(post_data)
        print(type(post_data))
        print(type(post_data["post_content"]))

        if post_data is None:
            response = jsonify(
                {
                    "self": f"/posts",
                    "added": False,
                    "post": None,
                    "error": "the request body isn't populated",
                }
            )
            response.status_code = 400
            return response
        post_to_add = Post(post_data)

        print("post to add")
        print(post_to_add)
        print(type(post_to_add))

        post_added_successfully: bool = PostDao.add_post(new_post=post_to_add)
        print(post_added_successfully)

        if post_added_successfully:
            post_added = PostDao.get_post_by_id(post_to_add.post_id)
            print("post added type")
            print(type(post_added))
            post_added_dict: dict = post_added.to_dict()

            print("post_added_dict")
            print(post_added_dict)
            response = jsonify(
                {
                    "self": "/posts",
                    "added": True,
                    "post": post_added_dict,
                }
            )
            print(response)
            # return post_added_dict, 200
            return Response(post_added_dict, mimetype="application/json", status=200)
        else:
            response = jsonify(
                {
                    "self": "/posts",
                    "added": False,
                    "post": None,
                    "error": "failed to create a new post",
                }
            )
            response.status_code = 500
            return response


class PostsByThreadApi(Resource):

    # def get_posts_count(self, obj):
    #    return PostDao.objects.filter(thread__forum=obj).count()

    post_last_activity_fields = {
        "thread": fields.Integer,
        # "thread_name": fields.String,
        # "activity_time": fields.DateTime,
        # "pinned": fields.Boolean,
        "post_creator_name": fields.String,
    }

    resource_fields = {
        "post_id": fields.Integer,
        "post_content": fields.String,
        "post_created_at": fields.String,
        "post_updated_at": fields.String,
        "post_creator_name": fields.String,
        "post_creator": fields.String,
        "avatar": fields.String
        # "post_count": fields.Integer,
        # "last_activity": fields.Nested(thread_last_activity_fields),
        # "last_activity": {
        #    "thread_id": fields.Integer,
        #    "thread_name": fields.String,
        #    "post_created_at": fields.String,
        #    "post_creator_name": fields.String,
        #    "pinned": fields.String,
        # },
    }

    @marshal_with(resource_fields)
    # @jwt_required()
    def get(self, thread_id: int):
        """
        Get all the posts by thread in the database.
        :return: A response object for the GET API request.
        """
        print("in routes///////////////////")

        posts: list = PostDao.get_posts_by_thread(thread_id)
        print(type(posts))
        print(posts)
        for post in posts:
            print(post)

        # res = threads_schema.dump(threads)
        # print(res)
        return posts
