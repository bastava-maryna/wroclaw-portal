"""download data needed to fill uni db"""
import sqlite3
from urllib.error import URLError
from sqlalchemy.inspection import inspect

from collections import defaultdict

# import dpath.util

from src.utils.validators import validate_string
from src.utils.helpers import get_json_from_url
from src.utils.helpers import sql_data_to_dict

# get column names from table
# columns = [column.name for column in inspect(model).c]


FORUM_DATA_URL = "http://localhoat/forum"


users_sample_data = [
    ("User 1", "user1@gmail.com", "user1"),
]


# *************************************************************************************
# @app.before_first_request
def fill_forum_tables(db):
    """function to initial fill database forum tables"""

    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    cursor.executemany(USERS_QUERY, users_sample_data)
    conn.commit()
    print("users table filled +++++++++++++++++++++++++++++++++++++++++")

    conn.close()
