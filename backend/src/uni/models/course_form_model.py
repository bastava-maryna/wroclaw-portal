"""course_forms  model"""
from main import db, ma
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class CourseForm(db.Base):
    "course_forms table schema"
    __tablename__ = "course_forms"

    course_form_id = Column(Integer, primary_key=True)
    course_form_name = Column(String(64), index=True, unique=True)

    # course = relationship("Course", backref="courses")

    def __init__(self, course_form_name: str):
        self.course_form_name = course_form_name

    def __repr__(self):
        """
        String representation of the course form.
        This representation is meant to be machine readable.
        :return: The course form string.
        """
        return f"<CourseForm {self.course_form_name}>"

    def __str__(self):
        """
        String representation of the course form.
        This representation is meant to be human readable.
        :return: The course form string.
        """
        return (
            f"CourseForm: [course_form_id: {self.course_form_id},"
            f"course_form_name: {self.course_form_name}]"
        )


class CourseFormSchema(ma.Schema):
    class Meta:
        model = CourseForm


course_form_schema = CourseFormSchema()
course_forms_schema = CourseFormSchema(many=True)
