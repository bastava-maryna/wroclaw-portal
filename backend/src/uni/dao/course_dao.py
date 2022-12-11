"""courses data access from the database.  Contains SQL queries related to courses."""
from typing import List
from main import db
from sqlalchemy import and_

from src.uni.dao.basic_dao import BasicDao
from src.uni.models.course_model import Course
from src.uni.models.course_form_model import CourseForm
from src.uni.models.course_language_model import CourseLanguage
from src.uni.models.course_level_model import CourseLevel
from src.uni.models.course_title_model import CourseTitle


class CourseDao:
    @staticmethod
    def get_courses() -> List[Course]:
        """
        Get a list of all the courses in the database.
        :return: A list containing Course model objects.
        """

        return Course.query.order_by(Course.course_name).all()

    @staticmethod
    def get_courses_by_name(course_name: str) -> List[Course]:
        """
        Get a list of all the courses from the database based on their name.
        :param study_name: Study name
        :return: The result of the database query.
        """
        return Course.query.filter_by(course_name=course_name).all()

    @staticmethod
    def get_course_by_id(course_id: str) -> Course:
        """
        Get a single course from the database based on their id.
        :param id: Id which uniquely identifies the course.
        :return: The result of the database query.
        """
        return Course.query.filter_by(course_id=course_id).first()

    @staticmethod
    def add_course(course: Course) -> bool:
        """
        Add a course.
        :param course: Object representing a course for the application.
        :return: True if the course is inserted into the database, False otherwise.
        """
        db.session.add(course)
        return BasicDao.safe_commit()

    @staticmethod
    def update_course(course_id: int, course: Course) -> bool:
        """
        Update a course in the database.
        :param course_id: Course id which uniquely identifies the course.
        :param course: Object representing an updated course for the application.
        :return: True if the course is updated in the database, False otherwise.
        """
        db.session.execute(
            """
            UPDATE courses SET
                course_name=:course_name,
            WHERE course_id=:course_id
            """,
            {
                "course_name": course.course_name,
            },
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_course(course_id: int) -> bool:
        """
        Delete a course from the database based on its id.
        :param course_id: Course id which uniquely identifies the course.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            "DELETE FROM courses WHERE course_id=:course_id",
            {"course_id": course_id},
            # bind=UniDao.engine,
        )

        return BasicDao.safe_commit()

    @staticmethod
    def filter_courses(params: dict) -> List[Course]:
        """method to filter courses using parameners from query string"""

        query = (
            Course.query.join(CourseLanguage)
            .join(CourseForm)
            .join(CourseTitle)
            .join(CourseLevel)
            .filter(Course.institution == params["uni_uid"])
        )
        # .join(CourseLanguage, Course.language==CourseLanguage.course_language_id)
        # .join(CourseForm,Course.form==CourseForm.course_form_id)
        # .join(CourseTitle,Course.title==CourseForm.course_form_id)

        # .with_entities(
        #    Course.course_id,
        #    Course.course_name,
        #    Course.main_discipline,
        #    Course.semesters_number,
        #    Course.ects,
        #    CourseForm.course_form_name,
        #    CourseLanguage.course_language_name,
        #    CourseTitle.course_title_name,
        # )

        if "search" in params:
            search = "%{}%".format(params["search"])
            query = query.filter(
                # Course.course_name == params["search"],
                Course.course_name.ilike(search)
            )
        else:
            if "discipline_name" in params:
                query = query.filter(
                    Course.main_discipline == params["discipline_name"],
                )
            if "level" in params:
                query = query.filter(
                    Course.level == params["level"],
                )

        result = query.all()

        return result
