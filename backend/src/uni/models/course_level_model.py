"""course_levels  model"""
from main import db, ma
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class CourseLevel(db.Base):
    "course_levels table schema"
    __tablename__ = "course_levels"

    course_level_id = Column(Integer, primary_key=True)
    course_level_name = Column(String(64), index=True, unique=True)

    # course = relationship("Course", backref="courses")

    def __init__(self, course_level_name: str):
        self.course_level_name = course_level_name

    # def json(self):
    #  return {'name':self.name,...}
    def __repr__(self):
        """
        String representation of the course level.
        This representation is meant to be machine readable.
        :return: The course level string.
        """
        return f"<CourseLevel {self.course_level_name}>"

    def __str__(self):
        """
        String representation of the course level.
        This representation is meant to be human readable.
        :return: The course level string.
        """
        return (
            f"CourseLevel: [course_level_id: {self.course_level_id},"
            f"course_level_name: {self.course_level_name}]"
        )


class CourseLevelSchema(ma.Schema):
    """schema for CourseLevel"""

    class Meta:
        model = CourseLevel


course_level_schema = CourseLevelSchema()
course_levels_schema = CourseLevelSchema(many=True)
