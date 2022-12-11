"""users table schema"""
from main import db, ma
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime,
    Boolean,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from marshmallow import fields


class Role(Enum):
    USER = "User"
    ADMIN = "Admin"


class User(db.Base):
    "users table schema"
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False, unique=True)
    user_email = Column(String(64), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    avatar = Column(Text)
    # role = Column(Enum(Role))
    # created_on=Column(DateTime(timezone=True), server_default=func.now())
    # last_login=Column(DateTime(timezone=True), onupdate=func.now())
    threads = relationship(
        "Thread", backref="Tread", lazy="dynamic", cascade="all,delete-orphan"
    )
    posts = relationship("Post", backref="Post", lazy=True, cascade="all,delete-orphan")

    def __init__(self, user: dict):
        self.user_name = user.get("user_name")
        self.user_email = user.get("user_email")
        self.password = user.get("password")
        self.avatar = user.get("avatar")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def json(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "avatar": self.avatar,
        }

    def __repr__(self):
        """
        String representation of the user.
        This representation is meant to be machine readable.
        :return: The user string.
        """
        return f"<User {self.user_name}"

    def __str__(self):
        """
        String representation of the user.
        This representation is meant to be human readable.
        :return: The user string.
        """
        return (
            f"User: [user_id: {self.user_id},user_name: {self.user_name},"
            f"user_email:{self.user_email},password:{self.password},"
            f"avatar:{self.avatar}]"
        )


class UserSchema(ma.Schema):
    """schema for User"""

    class Meta:
        model = User
        sqla_session = db.session
        # ordered = True
        fields = ("user_id", "user_name", "user_email", "avatar")
        # load_instance = True

    # user_id = fields.Integer()
    # user_name = fields.String()
    # user_email = fields.String()
    # password = fields.String()
    # avatar = fields.String()
    # threads = fields.Nested(ThreadSchema, many=True)


class UserShortSchema(ma.Schema):
    """schema for User without password"""

    class Meta:
        model = User
        sqla_session = db.session

    fields = ("user_name", "user_email", "avatar")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_short_schema = UserShortSchema()
