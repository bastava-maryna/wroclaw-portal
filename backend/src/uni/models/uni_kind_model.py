"""uni_kinds  model"""
from main import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class UniKind(db.Base):
    "uni_kinds table schema"
    __tablename__ = "uni_kinds"

    kind_id = Column(Integer, primary_key=True)
    kind_name = Column(String(64), index=True, unique=True)
    unis = relationship("Uni", backref="kinds")

    def __init__(self, uni_kind: dict):
        self.kind_name = uni_kind.get("kind_name")

    def __repr__(self):
        """
        String representation of the uniiversity kind.
        This representation is meant to be machine readable.
        :return: The uni_kind string.
        """
        return f"<UniKind {self.kind_name}>"

    def __str__(self):
        """
        String representation of the university kind.
        This representation is meant to be human readable.
        :return: The uni kind string.
        """
        return f"UniKind: [kind_id: {self.kind_id},kind_name: {self.kind_name}]"
