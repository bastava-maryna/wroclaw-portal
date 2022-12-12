"""Topic data access from the database.
Contains SQL queries related to topic."""

from main import db
from src.uni.dao.basic_dao import BasicDao
from src.forum.models.topic_model import Topic


class TopicDao:
    """topic DAO"""

    @staticmethod
    def get_topics() -> list:
        """
        Retrieve all the topics in the database.
        :return: The result of the query.
        """
        return Topic.query.order_by(Topic.topic_name).all()

    @staticmethod
    def get_topic_by_id(topic_id: str) -> Topic:
        """
        Retrieve a single topic by its unique id
        :param topic_id: The unique identifier for a topic.
        :return: The result of the query.
        """
        return Topic.query.filter_by(topic_id=topic_id).first()

    @staticmethod
    def get_topic_by_name(topic_name: str) -> Topic:
        """
        Retrieve the topic on a specific name.
        :param topic_name: Name for a topic.
        :return: The result of the query.
        """
        return Topic.query.filter_by(topic_name=topic_name).first()

    @staticmethod
    def add_topic(new_topic: Topic) -> bool:
        """
        Add a topic to the database.
        :param new_topic: Object representing a topic.
        :return: True if the topic is inserted into the database, False otherwise.
        """
        db.session.add(new_topic)
        return BasicDao.safe_commit()

    @staticmethod
    def update_topic(topic: Topic) -> bool:
        """
        Update a topic in the database.
        :param topic: Object representing an updated topic.
        :return: True if the topic is updated in the database, False otherwise.
        """
        db.session.execute(
            """
            UPDATE topics SET
                topic_name=:topic_name,
            WHERE topic_id=:topic_id
            """,
            {
                "topic_id": topic.topic_id,
                "topic_name": topic.topic_name,
            },
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_topic_by_id(topic_id: str) -> bool:
        """
        Delete a topic from the database based on its id.
        :param topic_id: ID which uniquely identifies the topic.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            "DELETE FROM topics WHERE topic_id=:topic_id",
            {"topic_id": topic_id},
        )
        return BasicDao.safe_commit()

    @staticmethod
    def get_topics_info() -> list:
        """
        Get a topics from the database with information about number of treads and posts in each topic .
        :return: The result of the query.
        """
        result = db.session.execute(
            f"WITH threadpost AS "
            f"(SELECT thread_id,topic,COUNT(post_id) AS post_count "
            f"FROM threads LEFT JOIN posts ON thread_id=thread "
            f"GROUP BY thread_id) "
            f"SELECT topic_id,topic_name,description, "
            f"COUNT(thread_id) AS threads_count, SUM(post_count) AS posts_count "
            f"FROM topics LEFT JOIN threadpost ON threadpost.topic=topics.topic_id "
            f"GROUP BY topic_id,topic_name,description"
        ).fetchall()

        return result
