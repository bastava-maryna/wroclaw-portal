"""download data needed to fill uni db"""
import sqlite3
from urllib.error import URLError
from sqlalchemy.inspection import inspect
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source="pl", target="en")
import sqlite3

# pip install -U deep-translator
from collections import defaultdict

# import dpath.util

from src.utils.validators import validate_string
from src.utils.helpers import get_json_from_url
from src.utils.helpers import sql_data_to_dict
from src.uni import constants as CONST

# get column names from table
# columns = [column.name for column in inspect(model).c]


# here id already exist in sourse
def load_institutions(source: str):
    """data to fill the unis in database"""
    data = []
    token = ""
    is_continue = True

    # count = 1
    while is_continue:
        query_string = "?token=" + token if token else ""

        response = get_json_from_url(source + query_string)
        if response["results"]:
            token = response["pagination"]["token"]
        else:
            is_continue = False
            break

        # parse json data to SQL insert
        for item in response["results"]:

            status = item["statusCode"]
            country = item["country"]
            if item["iKindCd"]:
                kind = int(item["iKindCd"])
            else:
                kind = None

            # select universities in active status, i Poland, not Federation kind
            if (
                status == CONST.INSTITUTION_DATA_STATUS_FILTER
                and country == CONST.INSTITUTION_DATA_COUNTRY_FILTER
                and kind != CONST.INSTITUTION_DATA_KIND_FILTER
            ):

                uni_uid = validate_string(item["institutionUuid"])
                uni_name = validate_string(item["name"])
                www = validate_string(item["www"])
                phone_number = validate_string(item["phone"])
                uni_email = validate_string(item["eMail"])
                city = validate_string(item["city"])
                street = validate_string(item["street"])
                building = validate_string(item["bNumber"])
                postal_code = validate_string(item["postalCd"])
                voivodeship = int(item["voivodeshipCode"])

                elem = (
                    uni_uid,
                    uni_name,
                    kind,
                    www,
                    phone_number,
                    uni_email,
                    city,
                    street,
                    building,
                    postal_code,
                    voivodeship,
                )

                data.append(elem)

    return data


def load_courses_list(source: str):
    """get courses list to further proceed"""
    # return list of dict
    data = []
    token = ""
    is_continue = True

    while is_continue:
        query_string = "?token=" + token if token else ""

        response = get_json_from_url(source + query_string)
        if response["results"]:
            token = response["pagination"]["token"]
        else:
            is_continue = False
            break

        # parse json data to SQL insert
        for item in response["results"]:

            status = item["currentStatusCode"]

            if status == CONST.COURSE_DATA_STATUS_FILTER:  # prowadzone - active
                data.append(item)

    return data


def load_courses(course_list: list):
    """data to fill the courses table in database"""

    data = []

    # parse json data to SQL insert
    for item in course_list:
        isced_name = validate_string(item["iscedName"])
        institution = item["mainInstitutionUuid"]
        for disc in item["disciplines"]:
            if disc["disciplineLeading"] == "Tak":
                main_discipline = validate_string(disc["disciplineCode"])
        for elem in item["courseInstances"]:
            if elem["statusCode"] == "3":
                course_uid = validate_string(elem["courseInstanceUuid"])
                course_name = validate_string(item["courseName"])
                course_name = translator.translate(course_name)
                level = int(item["levelCode"])
                title = int(elem["titleCode"])
                form = int(elem["formCode"])
                language = validate_string(elem["languageCode"])
                semesters_number = int(elem["numberOfSemesters"])
                ects = int(elem["ects"])

                elem = (
                    course_uid,
                    course_name,
                    isced_name,
                    level,
                    title,
                    form,
                    language,
                    semesters_number,
                    ects,
                    main_discipline,
                    institution,
                )
                data.append(elem)

    return data


def courses_disciplines_data(courses: list, courses_dict: dict):
    """create data for courses_disciplines joint table in database"""
    data = []
    courses_dict_reversed = dict((v, k) for k, v in courses_dict.items())

    for item in courses:
        if "disciplines" in item:
            disciplines_list = item["disciplines"]
            for instance in item["courseInstances"]:
                course_uid = validate_string(instance["courseInstanceUuid"])
                if course_uid in courses_dict_reversed:
                    course_id = courses_dict_reversed[course_uid]
                else:
                    break
                for disc in disciplines_list:
                    elem = (course_id, disc["disciplineCode"])
                    data.append(elem)

    return data


data_to_load_dict = {}
data_to_load_dict["voivodeships"] = (CONST.VOIVODESHIP_DATA_URL, "voiv_id", "voiv_name")
data_to_load_dict["uni_kinds"] = (
    CONST.INSTITUTION_KINDS_DATA_URL,
    "kind_id",
    "kind_name",
)
data_to_load_dict["course_levels"] = (
    CONST.COURSE_LEVELS_DATA_URL,
    "course_level_id",
    "course_level_name",
)
data_to_load_dict["course_titles"] = (
    CONST.COURSE_TITLES_DATA_URL,
    "course_title_id",
    "course_title_name",
)
data_to_load_dict["course_forms"] = (
    CONST.COURSE_FORMS_DATA_URL,
    "course_form_id",
    "course_form_name",
)
data_to_load_dict["course_languages"] = (
    CONST.COURSE_LANGUAGES_DATA_URL,
    "course_language_id",
    "course_language_name",
)
data_to_load_dict["disciplines"] = (
    CONST.DISCIPLINES_DATA_URL,
    "discipline_id",
    "discipline_name",
)


# int, string id: in 2 tables(languages and disciplines) id-string
def load_dictionaries(initial_data: dict):
    """data to fill the dictionaries tables in database"""

    data = defaultdict(list)
    for k, v in initial_data.items():
        response = get_json_from_url(v[0])

        # parse json data to SQL insert
        for item in response:
            code = item["code"]
            name = validate_string(item["nameEn"])

            name = translator.translate(name)
            print(name)
            elem = (code, name)

            data[k].append(elem)

    return data


# *************************************************************************************
# @app.before_first_request
def fill_tables(db):
    """function to initial fill database tables"""

    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    # firstly delete old data
    cursor.execute(CONST.DELETE_COURSE_FORMS_TABLE_QUERY)
    cursor.execute(CONST.DELETE_COURSE_TITLES_TABLE_QUERY)
    cursor.execute(CONST.DELETE_COURSE_LANGUAGES_TABLE_QUERY)
    cursor.execute(CONST.DELETE_COURSE_LEVELS_TABLE_QUERY)
    cursor.execute(CONST.DELETE_COURSES_TABLE_QUERY)
    cursor.execute(CONST.DELETE_COURSES_DISCIPLINES_TABLE_QUERY)
    cursor.execute(CONST.DELETE_DISCIPLINES_TABLE_QUERY)
    cursor.execute(CONST.DELETE_UNI_KINDS_TABLE_QUERY)
    cursor.execute(CONST.DELETE_UNIS_TABLE_QUERY)
    cursor.execute(CONST.DELETE_VOIVODESHIPS_TABLE_QUERY)
    conn.commit()
    print("old data deleted-------------------------------------------------")

    loaded_dictionaries = load_dictionaries(data_to_load_dict)

    for k, v in data_to_load_dict.items():
        query = "INSERT INTO " + k + "(" + v[1] + "," + v[2] + ") VALUES (?,?)"
        cursor.executemany(query, loaded_dictionaries[k])
        conn.commit()
        print(k + " table filled")

    cursor.executemany(CONST.UNIS_QUERY, load_institutions(CONST.INSTITUTIONS_DATA_URL))
    conn.commit()
    print("unis table filled ======================================")

    courses_list = load_courses_list(CONST.COURSES_DATA_URL)
    print("courses list created-------------------------------------------------")

    courses_data = load_courses(courses_list)
    print("courses data created-------------------------------------------------")

    cursor.executemany(CONST.COURSES_QUERY, courses_data)
    conn.commit()
    print("courses table filled +++++++++++++++++++++++++++++++++++++++++")

    courses_dict_from_db = sql_data_to_dict(db, CONST.COURSES_SELECT_QUERY)
    print("courses query executed=========================================")

    cursor.executemany(
        CONST.COURSES_DISCIPLINES_QUERY,
        courses_disciplines_data(courses_list, courses_dict_from_db),
    )
    conn.commit()
    print(
        "courses disciplines joint table filled ======================================"
    )

    conn.close()
