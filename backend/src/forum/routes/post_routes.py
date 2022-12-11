"""Posts in the WroclawPortal API.
Used for retrieving, adding, updating, and deleting posts ."""
from flask_restful import Resource, fields, marshal_with
from flask import Response, request
from flask.json import jsonify
from src.forum.dao.post_dao import PostDao
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
    @jwt_required()
    def get(self, post_id):
        """
        Get a single post with a unique ID.
        :param post_id: The unique identifier for a post.
        :return: A response object for the GET API request.
        """
        post = PostDao.get_post_by_id(post_id=post_id)

        if post is None:
            response = jsonify(
                {
                    "self": f"/posts/{post_id}",
                    "post": None,
                    "error": "there is no post with this identifier",
                }
            )
            response.status_code = 400
            return response
        else:
            return post
            # return Response(response, mimetype="application/json", status=200)

    @jwt_required()
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
                    "error": "the post is equal to the existing post with the same id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

    @jwt_required()
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
    @jwt_required()
    def get(self):
        """
        Get all the posts in the database.
        :return: A response object for the GET API request.
        """
        print("in routes///////////////////")
        posts: list = PostDao.get_posts()

        if posts is None:
            response = jsonify(
                {
                    "self": "/posts",
                    "posts": None,
                    "error": "an unexpected error occurred retrieving posts",
                }
            )

            return Response(response, mimetype="application/json", status=500)
        else:
            return posts

    @marshal_with(resource_fields)
    @jwt_required()
    def post(self):
        """
        Create a new post.
        :return: A response object for the POST API request.
        """
        post_data: dict = request.get_json()

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

        post_added_successfully: bool = PostDao.add_post(new_post=post_to_add)

        if post_added_successfully:
            post_added = PostDao.get_post_by_id(post_to_add.post_id)
            post_added_dict: dict = post_added.to_dict()

            response = jsonify(
                {
                    "self": "/posts",
                    "added": True,
                    "post": post_added_dict,
                }
            )

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
    @jwt_required()
    def get(self, thread_id: int):
        """
        Get all the posts by thread in the database.
        :return: A response object for the GET API request.
        """
        print("in post by thread routes///////////////////")

        posts: list = PostDao.get_posts_by_thread(thread_id)

        # res = threads_schema.dump(threads)
        # print(res)
        return posts
        # return Response(posts, mimetype="application/json", status=200)
