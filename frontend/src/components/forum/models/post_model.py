"""post table shema"""
from main import db, ma
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func


class Post(db.Base):
    "posts table schema"
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    post_content = Column(Text)
    post_created_at = Column(DateTime(timezone=True), server_default=func.now())
    post_updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    thread = Column(Integer, ForeignKey("threads.thread_id"))
    post_creator = Column(Integer, ForeignKey("users.user_id"))

    def __init__(self, post: dict):
        self.post_content = post.get("post_content")
        self.post_created_at = post.get("post_created_at")
        self.post_updated_at = post.get("post_updated_at")
        self.thread = post.get("thread")
        self.post_creator = post.get("post_creator")

    def __repr__(self):
        """
        String representation of the post.
        This representation is meant to be machine readable.
        :return: The post string.
        """
        return f"<Post {self.post_content}"

    def __str__(self):
        """
        String representation of the post.
        This representation is meant to be human readable.
        :return: The post string.
        """
        return (
            f"Post: [post_id: {self.post_id},post_content: {self.post_content},"
            f"post_created_at:{self.post_created_at},post_updated_at:{self.post_updated_at},"
            f"thread: {self.thread},post_creator: {self.post_creator}]"
        )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PostSchema(ma.Schema):
    """schema for Post"""

    class Meta:
        model = Post


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
