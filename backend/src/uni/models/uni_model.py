"""uni table shema"""
from main import db, ma
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Uni(db.Base):
    "unis table schema"
    __tablename__ = "unis"

    uni_id = Column(Integer, primary_key=True)
    uni_uid = Column(String(30), unique=True)
    uni_name = Column(String(64), index=True, unique=True)
    kind = Column(Integer, ForeignKey("uni_kinds.kind_id"))
    www = Column(String(64))
    phone_number = Column(String(20))
    uni_email = Column(String(120), index=True)
    city = Column(String(64))
    street = Column(String(80))
    building = Column(String(10))
    postal_code = Column(String(6))
    voivodeship = Column(Integer, ForeignKey("voivodeships.voiv_id"))

    courses = relationship("Course", backref="courses")

    def __init__(self, uni: dict):
        self.uni_uid = uni.get("uni_uid")
        self.uni_name = uni.get("uni_name")
        self.kind = uni.get("kind")
        self.www = uni.get("www")
        self.phone_number = uni.get("phone_number")
        self.uni_email = uni.get("uni_email")
        self.city = uni.get("city")
        self.street = uni.get("street")
        self.building = uni.get("building")
        self.postal_code = uni.get("postal_code")
        self.voivodeship = uni.get("voivodeship")

    # def json(self):
    #  return {'name':self.name,...}
    def __repr__(self):
        """
        String representation of the uni.
        This representation is meant to be machine readable.
        :return: The uni string.
        """
        return f"<Uni {self.uni_name}"

    def __str__(self):
        """
        String representation of the uni.
        This representation is meant to be human readable.
        :return: The uni string.
        """
        return (
            f"Uni: [uni_id: {self.uni_id},uni_uid: {self.uni_uid},"
            f"uni_name: {self.uni_name},kind:{self.kind},"
            f"www: {self.www},phone_number: {self.phone_number},"
            f"uni_email: {self.uni_email},city: {self.city},street: {self.street},"
            f"building: {self.building},postal_code:{self.postal_code},"
            f"voivodeship:{self.voivodeship}]"
        )


# def json(self):
#    return {"name":self.name,...}


class UniSchema(ma.Schema):
    """schema for Uni"""

    class Meta:
        model = Uni


uni_schema = UniSchema()
unis_schema = UniSchema(many=True)


class CitiesSchema(ma.Schema):
    class Meta:
        model = Uni


cities_schema = CitiesSchema(many=True)
