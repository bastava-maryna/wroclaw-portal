"""course_titles  model"""
from main import db, ma
from sqlalchemy import Column, Integer, String


class CourseTitle(db.Base):
    "course_titles table schema"
    __tablename__ = "course_titles"

    course_title_id = Column(Integer, primary_key=True)
    course_title_name = Column(String(64), index=True, unique=True)

    # course = relationship("Course", backref="courses")

    def __init__(self, course_title_name: str):
        self.course_title_name = course_title_name

    def __repr__(self):
        """
        String representation of the course title.
        This representation is meant to be machine readable.
        :return: The course title string.
        """
        return f"<CourseTitle {self.course_title_name}>"

    def __str__(self):
        """
        String representation of the course title.
        This representation is meant to be human readable.
        :return: The course title string.
        """
        return (
            f"CourseTitle: [course_title_id: {self.course_title_id},"
            f"course_title_name: {self.course_title_name}]"
        )


class CourseTitleSchema(ma.Schema):
    """schema for CourseTitle"""

    class Meta:
        model = CourseTitle


course_title_schema = CourseTitleSchema()
course_titles_schema = CourseTitleSchema(many=True)
