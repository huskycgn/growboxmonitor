import requests
import mariadb
import datetime
from cred import *


def get_shelly_pwr():
    api_key = SHELLY_API_KEY
    parameters = {"id": SHELLY_ID_PLUG, "auth_key": api_key}

    base_url = "https://shelly-77-eu.shelly.cloud/device/status"

    response = requests.get(url=base_url, params=parameters)
    json_data = response.json()
    # print(json_data)
    consumption = float(json_data["data"]["device_status"]["switch:0"]["apower"])
    return consumption


def gettemp():
    api_key = SHELLY_API_KEY
    parameters = {"id": SHELLY_ID_HT, "auth_key": api_key}

    base_url = "https://shelly-77-eu.shelly.cloud/device/status"

    response = requests.get(url=base_url, params=parameters)
    json_data = response.json()
    output_dict = {}
    temp = float(json_data["data"]["device_status"]["temperature:0"]["tC"])
    humid = float(json_data["data"]["device_status"]["humidity:0"]["rh"])
    output_dict["temp"] = temp
    output_dict["humid"] = humid
    return output_dict


def getutc():
    return datetime.datetime.utcnow()


def write_energydb(table) -> None:
    """Executes SQL statements
    :param table, con:
    :return:
    """
    connection = mariadb.connect(
        host=db_host, user=db_user, password=db_pass, database=db_name
    )
    statement = f"INSERT INTO {table} (time, pwrcon, temp, humidity) VALUES('{getutc()}', {get_shelly_pwr()}, {gettemp()['temp']}, {gettemp()['humid']});"
    # print(statement)
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    return None



