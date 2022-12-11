"""Post data access from the database.
Contains SQL queries related to post."""

from main import db
from typing import List

from src.uni.dao.basic_dao import BasicDao
from src.forum.models.post_model import Post


class PostDao:
    """post DAO"""

    @staticmethod
    def get_posts() -> List[Post]:
        """
        Retrieve all the posts in the database.
        :return: The result of the query.
        """

        return Post.query.order_by(Post.post_created_at).all()

    @staticmethod
    def get_post_by_id(post_id: int) -> Post:
        """
        Retrieve a single post by its unique id
        :param post_id: The unique identifier for a post.
        :return: The result of the query.
        """

        return Post.query.filter_by(post_id=post_id).first()

    @staticmethod
    def get_posts_by_user_name(user_name: str) -> List[Post]:
        """
        Retrieve a posts by its user name
        :param user_name: The unique identifier for a user.
        :return: The result of the query.
        """

        return Post.query.filter_by(post_creator=user_name).all()

    @staticmethod
    def add_post(new_post: Post) -> bool:
        """
        Add a post to the database.
        :param new_post: Object representing a post.
        :return: True if the post is inserted into the database, False otherwise.
        """
        db.session.add(new_post)
        return BasicDao.safe_commit()

    @staticmethod
    def update_post(post: Post) -> bool:
        """
        Update a post in the database.
        :param post: Object representing an updated post.
        :return: True if the post is updated in the database, False otherwise.
        """
        db.session.execute(
            """
            UPDATE posts SET
                post_content=:post_comtent,
                post_updated_at=:post_updated_at
            WHERE post_id=:post_id
            """,
            {
                "post_id": post.post_id,
                "post_content": post.post_content,
                "post_updated_at": post.post_updated_at,
            },
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_post_by_id(post_id: int) -> bool:
        """
        Delete a post from the database based on its id.
        :param post_id: ID which uniquely identifies the post.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            "DELETE FROM posts WHERE post_id=:post_id",
            {"post_id": post_id},
        )
        return BasicDao.safe_commit()

    @staticmethod
    def get_posts_count(self, thread_id: int):
        return Post.query.filter_by(thread_id=thread_id).count()

    @staticmethod
    def get_posts_by_thread(thread_id: int) -> list:
        """
        Retrieve all the threads of one topic in the database by topic id.
        :param topic_id: The unique identifier for a topic.
        :return: The result of the query.
        """

        result = db.session.execute(
            f"SELECT thread_id,thread_creator, post_id,post_content, "
            f"post_created_at,post_updated_at,post_creator, "
            f"u2.user_name as post_creator_name, u2.avatar as avatar "
            f"FROM threads JOIN posts ON thread_id=thread "
            f"JOIN users AS u2 ON u2.user_id=post_creator "
            f"WHERE thread_id=:thread_id",
            {"thread_id": thread_id},
        ).fetchall()

        return result
