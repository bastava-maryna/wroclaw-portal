"""course table shema"""

from main import db, ma
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


courses_disciplines = Table(
    "courses_disciplines",
    db.Base.metadata,
    Column("course_id_joint", Integer, ForeignKey("courses.course_id")),
    Column(
        "discipline_id_joint",
        String(10),
        ForeignKey("disciplines.discipline_id"),
    ),
)


class Course(db.Base):
    "courses table schema"
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True)
    course_uid = Column(String(30))
    course_name = Column(String(64), index=True)
    course_isced_name = Column(String(64))
    level = Column(Integer, ForeignKey("course_levels.course_level_id"))
    title = Column(Integer, ForeignKey("course_titles.course_title_id"))
    form = Column(Integer, ForeignKey("course_forms.course_form_id"))
    language = Column(String(10), ForeignKey("course_languages.course_language_id"))
    semesters_number = Column(Integer)
    ects = Column(Integer)
    main_discipline = Column(String(10))
    institution = Column(String(30), ForeignKey("unis.uni_uid"))
    course_disciplines = relationship(
        "Discipline", secondary=courses_disciplines, backref="courses", lazy="dynamic"
    )

    def __init__(self, course: dict):
        self.course_uid = course.get("course_uid")
        self.course_name = course.get("course_name")
        self.course_isced_name = course.get("course_isced_name")
        self.level = course.get("level")
        self.title = course.get("title")
        self.form = course.get("form")
        self.language = course.get("language")
        self.semesters_number = course.get("senesters_number")
        self.ects = course.get("ects")
        self.main_discipline = course.get("main_discipline")
        self.institution = course.get("institution")

    # def json(self):
    #  return {
    # 'name':self.name,"study_disciplines"=[study_discipline.json()
    # for study_discipline in self.study_disciplines.all()]}

    def __repr__(self):
        """
        String representation of the course.
        This representation is meant to be machine readable.
        :return: The course string.
        """
        return f"<Course {self.course_name}"

    def __str__(self):
        """
        String representation of the course.
        This representation is meant to be human readable.
        :return: The course string.
        """
        return (
            f"Course: [course_id: {self.course_id},course_uid: {self.course_uid},"
            f"course_name: {self.course_name},"
            f"course_isced_name: {self.course_isced_name},"
            f"level:{self.level},title: {self.title},"
            f"form: {self.form},language: {self.language},"
            f"semesters_number: {self.semesters_number}, ects:{self.ects},"
            f"main_discipline:{self.main_discipline},institution:{self.institution}]"
        )


class CourseSchema(ma.Schema):
    """schema for Course"""

    class Meta:
        model = Course
        # sqla_session = db.session
        # load_instance = True
        # fields = ["level"]


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
