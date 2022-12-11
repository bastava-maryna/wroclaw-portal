from os import environ


# UNI_DATA_API_URL = environ.get("UNI_DATA_API_URL")

UNI_DATA_API_URL = "https://radon.nauka.gov.pl/opendata/polon"
"""endpoints to load data"""
VOIVODESHIP_DATA_URL = UNI_DATA_API_URL + "/dictionaries/shared/voivodeships"
INSTITUTION_KINDS_DATA_URL = (
    UNI_DATA_API_URL + "/dictionaries/institution/institutionKinds"
)

COURSE_LEVELS_DATA_URL = UNI_DATA_API_URL + "/dictionaries/course/levels"
COURSE_TITLES_DATA_URL = UNI_DATA_API_URL + "/dictionaries/course/professionalTitles"
COURSE_FORMS_DATA_URL = UNI_DATA_API_URL + "/dictionaries/course/instanceForms"
COURSE_LANGUAGES_DATA_URL = (
    UNI_DATA_API_URL + "/dictionaries/course/philologicalLanguages"
)
DISCIPLINES_DATA_URL = UNI_DATA_API_URL + "/dictionaries/shared/disciplines"
COURSES_DATA_URL = UNI_DATA_API_URL + "/courses"
INSTITUTIONS_DATA_URL = UNI_DATA_API_URL + "/institutions"


"""sql querise to fill database tables"""
VOIVODESHIPS_QUERY = "INSERT INTO voivodeships(voiv_id,voiv_name) VALUES (?,?)"
INSTITUTION_KINDS_QUERY = "INSERT INTO uni_kinds(kind_id,kind_name) VALUES (?,?)"
COURSE_LEVELS_QUERY = (
    "INSERT INTO course_levels(course_level_id,course_level_name) VALUES (?,?)"
)

COURSE_TITLES_QUERY = (
    "INSERT INTO course_titles(course_title_id,course_title_name) VALUES (?,?)"
)
COURSE_FORMS_QUERY = (
    "INSERT INTO course_forms(course_form_id,course_form_name) VALUES (?,?)"
)
COURSE_LANGUAGES_QUERY = (
    "INSERT INTO course_languages(course_language_id,course_language_name) VALUES (?,?)"
)
DISCIPLINES_QUERY = (
    "INSERT INTO disciplines(discipline_id,discipline_name) VALUES (?,?)"
)

COURSES_QUERY = "INSERT INTO courses(course_uid,course_name,course_isced_name,level,title,form,language,semesters_number,ects,main_discipline,institution) VALUES (?,?,?,?,?,?,?,?,?,?,?)"

UNIS_QUERY = "INSERT INTO unis(uni_uid,uni_name,kind,www,phone_number,uni_email,city,street,building,postal_code,voivodeship)  VALUES (?,?,?,?,?,?,?,?,?,?,?)"

COURSES_DISCIPLINES_QUERY = (
    "INSERT INTO courses_disciplines(course_id_joint,discipline_id_joint) VALUES (?,?)"
)

COURSES_SELECT_QUERY = "SELECT course_id, course_uid FROM courses"

"""load only actual universities data (status=1 means Działająca - Operating)"""
INSTITUTION_DATA_STATUS_FILTER = "1"
"""load only Polish universities"""
INSTITUTION_DATA_COUNTRY_FILTER = "Polska"
"""exclude Frderation universities"""
INSTITUTION_DATA_KIND_FILTER = 16
"""load only actual courses data (status=3 means prowadzone - active)"""
COURSE_DATA_STATUS_FILTER = "3"


DELETE_COURSE_FORMS_TABLE_QUERY = "DELETE FROM course_forms"
DELETE_COURSE_LEVELS_TABLE_QUERY = "DELETE FROM course_levels"
DELETE_COURSE_LANGUAGES_TABLE_QUERY = "DELETE FROM course_languages"
DELETE_COURSE_TITLES_TABLE_QUERY = "DELETE FROM course_titles"
DELETE_COURSES_TABLE_QUERY = "DELETE FROM courses"
DELETE_COURSES_DISCIPLINES_TABLE_QUERY = "DELETE FROM courses_disciplines"
DELETE_DISCIPLINES_TABLE_QUERY = "DELETE FROM disciplines"
DELETE_UNI_KINDS_TABLE_QUERY = "DELETE FROM uni_kinds"
DELETE_UNIS_TABLE_QUERY = "DELETE FROM unis"
DELETE_VOIVODESHIPS_TABLE_QUERY = "DELETE FROM voivodeships"
