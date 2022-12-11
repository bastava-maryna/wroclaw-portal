"""Disciplene data access from the database.
Contains SQL queries related to discipline."""

from main import db

from src.uni.dao.basic_dao import BasicDao
from src.uni.models.discipline_model import Discipline


class DisciplineDao:
    """discipline DAO"""

    @staticmethod
    def get_disciplines() -> list:
        """
        Retrieve all the disciplines in the database.
        :return: The result of the query.
        """
        return Discipline.query.order_by(Discipline.discipline_name).all()

    @staticmethod
    def get_discipline_by_id(disc_id: str) -> Discipline:
        """
        Retrieve a single discipline by its unique id
        :param disc_id: The unique identifier for a discipline.
        :return: The result of the query.
        """
        return Discipline.query.filter_by(disc_id=disc_id).first()

    @staticmethod
    def get_discipline_by_name(disc_name: str) -> Discipline:
        """
        Retrieve the discipline on a specific name.
        :param disc_name: Name for a discipline.
        :return: The result of the query.
        """
        return Discipline.query.filter_by(disc_name=disc_name).first()

    @staticmethod
    def add_discipline(new_discipline: Discipline) -> bool:
        """
        Add a discipline to the database.
        :param new_disc: Object representing a discipline.
        :return: True if the discipline is inserted into the database, False otherwise.
        """
        db.session.add(new_discipline)
        return BasicDao.safe_commit()

    @staticmethod
    def update_discipline(discipline: Discipline) -> bool:
        """
        Update a discipline in the database.
        :param discipline: Object representing an updated discipline.
        :return: True if the discipline is updated in the database, False otherwise.
        """
        db.session.execute(
            """
            UPDATE disciplines SET
                discipline_name=:disc_name,
            WHERE disc_id=:disc_id
            """,
            {
                "disc_id": discipline.discipline_id,
                "discipline_name": discipline.discipline_name,
            },
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_discipline_by_id(disc_id: str) -> bool:
        """
        Delete a discipline from the database based on its id.
        :param disc_id: ID which uniquely identifies the discipline.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            "DELETE FROM disciplines WHERE discipline_id=:disc_id",
            {"discipline_id": disc_id},
        )
        return BasicDao.safe_commit()
