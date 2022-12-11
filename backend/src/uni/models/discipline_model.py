"""discipline  model"""
from main import db, ma
from sqlalchemy import Column, String

from src.uni.models.course_model import courses_disciplines


class Discipline(db.Base):
    "disciplines table schema"
    __tablename__ = "disciplines"

    discipline_id = Column(String(10), primary_key=True)
    discipline_name = Column(String(80), index=True)

    def __init__(self, discipline: dict):
        self.discipline_id = discipline.get("discipline_id")
        self.discipline_name = discipline.get("discipline_name")

    # def json(self):
    #  return {'name':self.name,...}
    def __repr__(self):
        """
        String representation of the discipline.
        This representation is meant to be machine readable.
        :return: The discipline string.
        """
        return f"<Discipline {self.discipline_name}"

    def __str__(self):
        """
        String representation of the discipline.
        This representation is meant to be human readable.
        :return: The discipline string.
        """
        return (
            f"Discipline: [discipline_id: {self.discipline_id}, "
            f"discipline_name: {self.discipline_name},]"
        )


class DisciplineSchema(ma.Schema):
    """schema for Discipline"""

    class Meta:
        model = Discipline


discipline_schema = DisciplineSchema()
disciplines_schema = DisciplineSchema(many=True)
