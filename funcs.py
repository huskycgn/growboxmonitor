import requests
import mariadb
import datetime
from cred import *


def get_shelly_pwr():
    api_key = SHELLY_API_KEY
    parameters = {"id": SHELLY_ID, "auth_key": api_key}

    base_url = "https://shelly-77-eu.shelly.cloud/device/status"

    response = requests.get(url=base_url, params=parameters)
    json_data = response.json()
    # print(json_data)
    consumption = float(json_data["data"]["device_status"]["switch:0"]["apower"])
    return consumption


def getpwr():
    pass


def gettemp():
    pass


def gethumid():
    pass


def getutc():
    return datetime.datetime.utcnow()


def write_energydb(table, con) -> None:
    """Executes SQL statements
    :param table, con:
    :return:
    """
    connection = mariadb.connect(
        host=db_host, user=db_user, password=db_pass, database=db_name
    )
    statement = f"INSERT INTO {table} (time, pwrcon) VALUES('{getutc()}', {get_shelly_pwr()});"

    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    return None