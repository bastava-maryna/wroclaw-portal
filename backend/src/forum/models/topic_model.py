"""topic table schema"""
from main import db, ma
from sqlalchemy import Column, Integer, String


class Topic(db.Base):
    "topics table schema"
    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True)
    topic_name = Column(String(255), index=True, unique=True)
    description = Column(String(100))
    slug = Column(String(255), unique=True)

    def __init__(self, topic: dict):
        self.topic_name = topic.get("topic_name")
        self.description = topic.get("description")
        self.slug = topic.get("slug")

    def __repr__(self):
        """
        String representation of the topic.
        This representation is meant to be machine readable.
        :return: The topc string.
        """
        return f"<Topic {self.topic_name}"

    def __str__(self):
        """
        String representation of the topic.
        This representation is meant to be human readable.
        :return: The topic string.
        """
        return (
            f"Topic: [topic_id: {self.topic_id},topic_name: {self.topic_name},"
            f"description:{self.description},slug:{self.slug}]"
        )


class TopicSchema(ma.Schema):
    """schema for Topic"""

    class Meta:
        model = Topic


topic_schema = TopicSchema()
topics_schema = TopicSchema(many=True)
