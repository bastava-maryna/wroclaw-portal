"""helpers methods common fpr application"""
# import urllib.request
import sqlite3
import json

# install passlib
from passlib.hash import pbkdf2_sha256 as sha256

# import requests
# from requests.exceptions import HTTPError
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import socket


def get_json_from_url(source: str):
    """load data from source url and tramsform it to json format"""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 Safari/537.36 YaBrowser/22.9.3.888 Yowser/2.5 Edge/18.19582"
    }
    request = Request(source, headers=headers or {})
    try:
        # with urlopen(source, timeout=100) as url:
        with urlopen(request, timeout=100) as response:
            # print(response.status)
            result = json.load(response)
            return result
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}, {http_err.status}, {http_err.code}")
    except URLError as url_error:
        if isinstance(url_error.reason, socket.timeout):
            # logging.error('socket timed out - URL %s', url)
            print(f"socket timed out - URL {url_error}")
            raise URLError(url_error.reason)
        else:
            print("some other error happened - URL {url_error}")
            raise URLError(url_error.reason)
    except Exception as err:
        print(f"Other error occurred: {err}")
        exit()


def sql_data_to_list_of_dicts(path_to_db, select_query):
    # def sql_data_to_list_of_dicts(connection, select_query):
    """Returns data from an SQL query as a list of dicts."""

    try:
        connection = sqlite3.connect(path_to_db)
        connection.row_factory = sqlite3.Row
        results = connection.execute(select_query).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in results]

        return unpacked
    except Exception as err:
        print(f"Failed to execute. Query: {select_query}\n with error:\n{err}")
        return []
    finally:
        connection.close()


def sql_data_to_dict(path_to_db, select_query):
    # def sql_data_to_list_of_dicts(connection, select_query):
    """Returns data from an SQL query as a list of dicts."""
    data = {}
    try:
        connection = sqlite3.connect(path_to_db)
        # connection.row_factory = sqlite3.Row
        results = connection.execute(select_query).fetchall()
        # unpacked = [{k: item[k] for k in item.keys()} for item in results]
        for row in results:
            data[row[0]] = row[1]

        return data
    except Exception as err:
        print(f"Failed to execute. Query: {select_query}\n with error:\n{err}")
        return []
    finally:
        connection.close()


def generate_hash(password):
    return sha256.hash(password)


def verify_hash(password, hash):
    return sha256.verify(password, hash)
