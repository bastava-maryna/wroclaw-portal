"""course_languages  model"""
from main import db, ma
from sqlalchemy import Column, String


class CourseLanguage(db.Base):
    "course_languages table schema"
    __tablename__ = "course_languages"

    course_language_id = Column(String(10), primary_key=True)
    course_language_name = Column(String(64), index=True, unique=True)

    # course = relationship("Course", backref="courses")

    def __init__(self, course_language: dict):
        self.course_language_id = course_language.get("course_language_id")
        self.course_language_name = course_language.get("course_language_name")

    def __repr__(self):
        """
        String representation of the course language.
        This representation is meant to be machine readable.
        :return: The course language string.
        """
        return f"<CourseLanguage {self.course_language_name}>"

    def __str__(self):
        """
        String representation of the course language.
        This representation is meant to be human readable.
        :return: The course language string.
        """
        return (
            f"CourseLanguage: [course_language_id: {self.course_language_id},"
            f"course_language_name: {self.course_language_name},]"
        )


class CourseLanguageSchema(ma.Schema):
    class Meta:
        model = CourseLanguage


course_language_schema = CourseLanguageSchema()
course_languages_schema = CourseLanguageSchema(many=True)
