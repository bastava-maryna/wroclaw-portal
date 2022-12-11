"""Uni data access from the database.  Contains SQL queries related to unis."""
from typing import List
from sqlalchemy import and_

from main import db

from src.uni.models.course_model import courses_disciplines
from src.uni.dao.basic_dao import BasicDao
from src.uni.models.uni_model import Uni
from src.uni.models.course_model import Course
from src.uni.models.discipline_model import Discipline
from src.uni.models.course_level_model import CourseLevel


class UniDao:
    """DAO for unis table"""

    @staticmethod
    def get_unis() -> List[Uni]:
        """
        Get a list of all the uniss in the database.
        :return: A list containing Uni model objects.
        """
        return Uni.query.all()

    @staticmethod
    def get_uni_by_name(uni_name: str) -> Uni:
        """
        Get a single uni from the database based on their name.
        :param uni_name: Uni name which uniquely identifies the uni.
        :return: The result of the database query.
        """
        return Uni.query.filter_by(uni_name=uni_name).first()

    @staticmethod
    def get_uni_by_id(uni_id: str) -> Uni:
        """
        Get a single uni from the database based on their id.
        :param id: Email which uniquely identifies the uni.
        :return: The result of the database query.
        """
        return Uni.query.filter_by(uni_id=uni_id).first()

    @staticmethod
    def get_uni_by_uid(uni_uid: str) -> Uni:
        """
        Get a single uni from the database based on their id.
        :param id: Email which uniquely identifies the uni.
        :return: The result of the database query.
        """

        return Uni.query.filter_by(uni_uid=uni_uid).first()

    @staticmethod
    def add_uni(uni: Uni) -> bool:
        """
        Add a uni.
        :param uni: Object representing a uni for the application.
        :return: True if the uni is inserted into the database, False otherwise.
        """
        db.session.add(uni)
        return BasicDao.safe_commit()

    @staticmethod
    def update_uni(uni_id: int, uni: Uni) -> bool:
        """
        Update a uni in the database.
        :param uni_id: Uni id which uniquely identifies the uni.
        :param uni: Object representing an updated uni for the application.
        :return: True if the uni is updated in the database, False otherwise.
        """
        db.session.execute(
            """
            UPDATE unis SET
                uni_name=:uni_name,
                uni_code=:uni_code,
                kind=:kind,
                www=:www,
                phone_number=:phone_number,
                uni_email=:uni_email,
                city=:city,
                street=:street,
                building=:building,
                postal_code=:postal_code
            WHERE uni_id=:uni_id
            """,
            {
                "uni_name": uni.uni_name,
                "kind": uni.kind,
                "www": uni.www,
                "phone_number": uni.phone_number,
                "uni_email": uni.uni_email,
                "city": uni.city,
                "street": uni.street,
                "building": uni.building,
                "postal_code": uni.postal_code,
            },
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_uni(uni_id: int) -> bool:
        """
        Delete a uni from the database based on its id.
        :param uni_id: Uni id which uniquely identifies the uni
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            "DELETE FROM unis WHERE uni_id=:uni_id",
            {"uni_id": uni_id},
        )

        return BasicDao.safe_commit()

    @staticmethod
    def get_cities() -> List[str]:
        """
        Get a list of all the cities in the database.
        :return: A list containing cities.
        """
        return Uni.query.with_entities(Uni.city).distinct().order_by(Uni.city).all()

    @staticmethod
    def filter_unis(params: dict) -> List[Uni]:

        query = (
            Course.query.join(
                courses_disciplines,
                courses_disciplines.c.course_id_joint == Course.course_id,
            )
            .join(
                Discipline,
                courses_disciplines.c.discipline_id_joint == Discipline.discipline_id,
            )
            .join(Uni, Uni.uni_uid == Course.institution)
            .join(CourseLevel, Course.level == CourseLevel.course_level_id)
            .with_entities(
                Uni.uni_name,
                Uni.uni_uid,
                Uni.city,
                Uni.street,
                Uni.building,
                Uni.postal_code,
                Uni.uni_email,
                Uni.phone_number,
                Uni.www,
                Course.course_id,
                Course.course_name,
                Course.level,
                Course.main_discipline,
                Discipline.discipline_id,
                Discipline.discipline_name,
                CourseLevel.course_level_name,
            )
        )
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
            if "city" in params:
                query = query.filter(
                    Uni.city == params["city"],
                )

        result = query.group_by(Uni.uni_uid).all()

        return result
