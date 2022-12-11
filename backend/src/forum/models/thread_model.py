"""thread table shema"""
from main import db, ma
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.sql import func
from src.user.user_model import UserSchema


class Thread(db.Base):
    "threads table schema"
    __tablename__ = "threads"

    thread_id = Column(Integer, primary_key=True)
    thread_name = Column(String(255), index=True, unique=True)
    thread_content = Column(Text)
    thread_created_at = Column(DateTime(timezone=True), server_default=func.now())
    thread_last_activity = Column(DateTime(timezone=True), default=func.now())
    topic = Column(Integer, ForeignKey("topics.topic_id"))
    thread_creator = Column(Integer, ForeignKey("users.user_id"))
    pinned = Column(Boolean, default=False)

    def __init__(self, thread: dict):
        self.thread_name = thread.get("thread_name")
        self.thread_content = thread.get("thread_content")
        self.thread_created_at = thread.get("thread_created_at")
        self.thread_last_activity = thread.get("thread_last_activity")
        self.topic = thread.get("topic")
        self.thread_creator = thread.get("thread_creator")
        self.pinned = thread.get("pinned")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        """
        String representation of the thread.
        This representation is meant to be machine readable.
        :return: The thread string.
        """
        return f"<Thread {self.thread_name}"

    def __str__(self):
        """
        String representation of the thread.
        This representation is meant to be human readable.
        :return: The thread string.
        """
        return (
            f"Thread: [thread_id: {self.thread_id},thread_name: {self.thread_name},"
            f"thread_content: {self.thread_content},"
            f"thread_created_at:{self.thread_created_at},"
            f"thread_last_activity: {self.thread_last_activity},topic: {self.topic},"
            f"thread_creator: {self.thread_creator},pinned: {self.pinned}]"
        )


class ThreadSchema(ma.Schema):
    """schema for Thread"""

    class Meta:
        model = Thread


class ThreadInfoSchema(ma.Schema):
    """schema for Thread"""

    user = ma.Nested(UserSchema)

    class Meta:
        model = Thread

    fields = (
        "tread_id",
        "tread_name",
        "thread_content",
        "topic",
        "tread_creator",
        "tread_created_at",
        "user",
    )
    ordered = True


thread_schema = ThreadSchema()
threads_schema = ThreadSchema(many=True)
thread_info_schema = ThreadInfoSchema()
