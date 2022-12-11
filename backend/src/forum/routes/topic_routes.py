"""Topic routes in the WroclawPortal API.
Used for retrieving, adding, updating, and deleting topics ."""
from flask_restful import Resource, fields, marshal_with
from flask import Response, request
from flask.json import jsonify
from src.forum.dao.topic_dao import TopicDao
from src.forum.dao.thread_dao import ThreadDao

# from flask_jwt_extended import jwt_required
from src.forum.models.topic_model import (
    Topic,
    TopicSchema,
    topic_schema,
    topics_schema,
)

resource_fields = {
    "topic_id": fields.Integer,
    "topic_name": fields.String,
    "description": fields.String,
    "slug": fields.String,
}


class TopicIdApi(Resource):
    @marshal_with(resource_fields)
    def get(self, topic_id):
        """
        Get a single topic with a unique ID.
        :param topic_id: The unique identifier for a topic.
        :return: A response object for the GET API request.
        """
        topic = TopicDao.get_topic_by_id(topic_id=topic_id)

        print(topic)
        return topic
        """
        if topic is None:
            response = jsonify(
                {
                    "self": f"/topics/{topic_id}",
                    "topic": None,
                    # "log": None,
                    "error": "there is no topic with this identifier",
                }
            )
            response.status_code = 400
            return response
        else:
            topic_dict: dict = Topic(topic).__dict__
            # comment_dict["time"] = str(comment_dict["time"])

            response = jsonify(
                {
                    "self": f"/topics/{topic_id}",
                    "topic": topic_dict,
                    # "log": f'/v2/logs/{comment_dict.get("log_id")}',
                }
            )
            # response.status_code = 200
            # return response
            return Response(response, mimetype="application/json", status=200)
        """

    def put(self, topic_id):
        """
        Update an existing topic.
        :param topic_id: The unique identifier for a topic.
        :return: A response object for the PUT API request.
        """
        old_topic: Topic = TopicDao.get_topic_by_id(topic_id=topic_id)

        if old_topic is None:
            response = jsonify(
                {
                    "self": f"/topics/{topic_id}",
                    "updated": False,
                    "topic": None,
                    "error": "there is no existing topic with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        topic_data: dict = request.get_json()
        new_topic = Topic(topic_data)

        if old_topic != new_topic:

            is_updated = TopicDao.update_topic(topic=new_topic)

            if is_updated:
                updated_topic: Topic = TopicDao.get_topic_by_id(
                    topic_id=new_topic.topic_id
                )
                updated_topic_dict: dict = Topic(updated_topic).__dict__

                response = jsonify(
                    {
                        "self": f"/topics/{topic_id}",
                        "updated": True,
                        "topic": updated_topic_dict,
                    }
                )

                return Response(response, mimetype="application/json", status=200)
            else:
                response = jsonify(
                    {
                        "self": f"/topics/{topic_id}",
                        "updated": False,
                        "topic": None,
                        "error": "the topic failed to update",
                    }
                )

                return Response(response, mimetype="application/json", status=500)
        else:
            response = jsonify(
                {
                    "self": f"/topics/{topic_id}",
                    "updated": False,
                    "topic": None,
                    "error": "the topic submitted is equal to the existing topic with the same id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

    def delete(self, topic_id):
        """
        Delete an existing topic.
        :param topic_id: The unique identifier for a topic.
        :return: A response object for the DELETE API request.
        """
        existing_topic: Topic = TopicDao.get_topic_by_id(topic_id=topic_id)

        if existing_topic is None:
            response = jsonify(
                {
                    "self": f"/topics/{topic_id}",
                    "deleted": False,
                    "error": "there is no existing topic with this id",
                }
            )

            return Response(response, mimetype="application/json", status=400)

        is_deleted = TopicDao.delete_topic_by_id(topic_id=topic_id)

        if is_deleted:
            response = jsonify(
                {
                    "self": f"/topics/{topic_id}",
                    "deleted": True,
                }
            )

            return Response(response, mimetype="application/json", status=204)
        else:
            response = jsonify(
                {
                    "self": f"/topics/{topic_id}",
                    "deleted": False,
                    "error": "failed to delete the topic",
                }
            )

            return Response(response, mimetype="application/json", status=500)


class TopicNameApi(Resource):

    # @jwt_required()
    def get(self, name):
        "get topic by name"

        topic = Topic.objects.get(name=name).to_json()
        return Response(topic, mimetype="application/json", status=200)

    def put(self, name):
        body = request.get_json()
        Topic.objects.get(name=name).update(**body)
        return "", 200

    def delete(self, name):

        topic = Topic.objects.get(name=name).delete()
        return "", 200


class TopicsApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        """
        Get all the topics in the database.
        :return: A response object for the GET API request.
        """
        print("in routes///////////////////")
        topics: list = TopicDao.get_topics()

        return topics
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

    def post(self):

        """
        Create a new discipline.
        :return: A response object for the POST API request.
        """
        topic_data: dict = request.get_json()

        if topic_data is None:
            response = jsonify(
                {
                    "self": f"/topics",
                    "added": False,
                    "topic": None,
                    "error": "the request body isn't populated",
                }
            )
            response.status_code = 400
            return response
        topic_to_add = Topic(topic_data)

        topic_added_successfully: bool = TopicDao.add_topic(new_topic=topic_to_add)

        if topic_added_successfully:
            topic_added = TopicDao.get_topic_by_id(topic_to_add.topic_id)
            topic_added_dict: dict = Topic(topic_added).__dict__

            response = jsonify(
                {
                    "self": "/topics",
                    "added": True,
                    "topic": topic_added_dict,
                }
            )
            response.status_code = 200
            return response
        else:
            response = jsonify(
                {
                    "self": "/topics",
                    "added": False,
                    "topic": None,
                    "error": "failed to create a new topic",
                }
            )
            response.status_code = 500
            return response


class TopicsInfoApi(Resource):
    thread_last_activity_fields = {
        "thread_id": fields.Integer,
        "thread_name": fields.String,
        "activity_time": fields.DateTime,
        "pinned": fields.Boolean,
        "thread_creator_name": fields.String,
    }

    resource_fields = {
        "topic_id": fields.Integer,
        "topic_name": fields.String,
        "description": fields.String,
        "slug": fields.String,
        "posts_count": fields.Integer,
        "threads_count": fields.Integer,
        # "last_activity": fields.Nested(thread_last_activity_fields),
    }

    topic_info = {}

    # def get_posts_count(self, obj):
    #    return PostDao.objects.filter(thread__forum=obj).count()

    @marshal_with(resource_fields)
    def get(self):
        """
        Get all the topics in the database.
        :return: A response object for the GET API request.
        """
        print("in routes///////////////////")
        topic_info = {}

        topics: list = TopicDao.get_topics_info()

        res = topics_schema.dump(topics)
        print(res)
        return topics
