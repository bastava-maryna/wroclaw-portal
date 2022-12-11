"""Thread data access from the database.
Contains SQL queries related to thread."""

from main import db
from typing import List

from src.uni.dao.basic_dao import BasicDao
from src.forum.models.thread_model import Thread
from src.user.user_model import User


class ThreadDao:
    """thread DAO"""

    @staticmethod
    def get_threads() -> List[Thread]:
        """
        Retrieve all the threads in the database.
        :return: The result of the query.
        """

        return Thread.query.order_by(Thread.thread_name).all()

    @staticmethod
    def get_thread_by_id(thread_id: str) -> Thread:
        """
        Retrieve a single thread by its unique id
        :param thread_id: The unique identifier for a thread.
        :return: The result of the query.
        """

        return Thread.query.filter_by(thread_id=thread_id).first()

    @staticmethod
    def get_thread_info_by_id(thread_id: str) -> Thread:
        """
        Retrieve a single thread by its unique id
        :param thread_id: The unique identifier for a thread.
        :return: The result of the query.
        """
        """
        res = (
            Thread.query.join(User, Thread.thread_creator == User.user_id)
            .filter(thread_id == thread_id)
            .with_entities(
                Thread.thread_id,
                Thread.thread_name,
                Thread.thread_content,
                Thread.thread_created_at,
                Thread.pinned,
                Thread.thread_creator,
                User.user_name,
                User.user_email,
                User.avatar,
            )
            .first()
        )
        """

        return Thread.query.join(User).filter(thread_id == thread_id).first()

    @staticmethod
    def get_thread_by_name(thread_name: str) -> Thread:
        """
        Retrieve the thread on a specific name.
        :param thread_name: Name for a thread.
        :return: The result of the query.
        """
        return Thread.query.filter_by(thread_name=thread_name).first()

    @staticmethod
    def add_thread(new_thread: Thread) -> bool:
        """
        Add a thread to the database.
        :param new_thread: Object representing a thread.
        :return: True if the thread is inserted into the database, False otherwise.
        """
        db.session.add(new_thread)
        return BasicDao.safe_commit()

    @staticmethod
    def update_thread(thread: Thread) -> bool:
        """
        Update a thread in the database.
        :param thread: Object representing an updated thread.
        :return: True if the thread is updated in the database, False otherwise.
        """
        db.session.execute(
            """
            UPDATE threads SET
                thread_name=:thread_name,
            WHERE thread_id=:thread_id
            """,
            {
                "thread_id": thread.thread_id,
                "thread_name": thread.thread_name,
            },
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_thread_by_id(thread_id: str) -> bool:
        """
        Delete a thread from the database based on its id.
        :param thread_id: ID which uniquely identifies the thread.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            "DELETE FROM threads WHERE thread_id=:thread_id",
            {"thread_id": thread_id},
        )
        return BasicDao.safe_commit()

    @staticmethod
    def get_threads_count(self, topic_id: int):
        return Thread.query.filter_by(topic_id=topic_id).count()

    @staticmethod
    def get_threads_by_topic(topic_id: int) -> list:
        """
        Retrieve all the threads of one topic in the database by topic id
        with thread_creator info and posts number by thread and last activity in thread.
        :param topic_id: The unique identifier for a topic.
        :return: The result of the query.
        """
        result = (
            db.session.execute(
                f"WITH threadpost AS "
                f"(SELECT thread_id, count(post_id) AS post_count "
                f"FROM threads LEFT JOIN posts ON thread_id=thread GROUP BY thread_id), "
                f"last_activity AS "
                f"(SELECT g.*, u2.user_name AS post_creator_name,u2.avatar as post_creator_avatar "
                f"FROM "
                f"(SELECT p.*,topic "
                f"FROM threads LEFT JOIN "
                f"(SELECT post_id, post_created_at, post_creator, thread ,row_number() "
                f"OVER (PARTITION BY thread ORDER BY post_created_at DESC) AS rn "
                f"FROM posts) AS p "
                f"ON threads.thread_id=p.thread where rn=1 or rn is null) AS g "
                f"LEFT JOIN users AS u2 ON u2.user_id=g.post_creator "
                f"WHERE g.topic={topic_id}) "
                f"SELECT threads.thread_id,thread_name, thread_created_at, "
                f"thread_creator, thread_content,pinned,threads.topic,post_count, "
                f"u1.user_name AS thread_creator_name,u1.avatar AS thread_creator_avatar, "
                f"post_creator,post_creator_name,post_created_at,post_id,post_creator_avatar "
                f"FROM threads "
                f"JOIN threadpost ON threadpost.thread_id=threads.thread_id "
                f"JOIN users AS u1 ON u1.user_id=thread_creator "
                f"LEFT JOIN last_activity ON threads.thread_id=last_activity.thread "
                f"WHERE threads.topic={topic_id} "
                f"ORDER BY thread_created_at DESC "
                # {"thread_id": topic_id},
            )
            .mappings()
            .all()
        )

        return result
