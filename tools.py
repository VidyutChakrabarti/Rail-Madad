from langchain.tools import tool 
from datetime import date
import http.client
import json
import os
from dotenv import load_dotenv
load_dotenv()
rapid_api_key = os.getenv('RAPID_API_KEY')

@tool("Get current date")
def getCurrentDate():
    """used to fetch the current date in a formatted manner."""
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    return d

conn = http.client.HTTPSConnection("indian-railway-irctc.p.rapidapi.com")
headers = {
    'x-rapidapi-key': rapid_api_key,
    'x-rapidapi-host': "indian-railway-irctc.p.rapidapi.com",
    'x-rapid-api': "rapid-api-database"
}

conn.request("GET", "/api/trains/v1/train/status?departure_date=20240827&isH5=true&client=web&train_number=11040", headers=headers)
res = conn.getresponse()
data = res.read()
json_data = json.loads(data.decode("utf-8"))
# print(json_data)

@tool("GetArrivalTime")
def getArrivalTime(train_status):
    try:
        arrival_time = train_status['body']['stations'][0]['arrivalTime']
        return arrival_time
    except KeyError:
        return "Data not available"

@tool("GetDepartureTime")
def getDepartureTime(train_status):
    try:
        departure_time = train_status['body']['stations'][0]['departureTime']
        return departure_time
    except KeyError:
        return "Data not available"

@tool("GetDistance")
def getDistance(train_status):
    try:
        distance = train_status['body']['stations'][0]['distance']
        return distance
    except KeyError:
        return "Data not available"

@tool("GetHaltTime")
def getHaltTime(train_status):
    try:
        halt_time = train_status['body']['stations'][0]['haltTime']
        return halt_time
    except KeyError:
        return "Data not available"

@tool("GetStationName")
def getStationName(train_status):
    try:
        station_name = train_status['body']['stations'][0]['stationName']
        return station_name
    except KeyError:
        return "Data not available"

@tool("GetStnSerialNumber")
def getStnSerialNumber(train_status):
    try:
        stn_serial_number = train_status['body']['stations'][0]['stnSerialNumber']
        return stn_serial_number
    except KeyError:
        return "Data not available"

@tool("GetActualArrivalDate")
def getActualArrivalDate(train_status):
    try:
        actual_arrival_date = train_status['body']['stations'][0]['actual_arrival_date']
        return actual_arrival_date
    except KeyError:
        return "Data not available"

@tool("GetActualArrivalTime")
def getActualArrivalTime(train_status):
    try:
        actual_arrival_time = train_status['body']['stations'][0]['actual_arrival_time']
        return actual_arrival_time
    except KeyError:
        return "Data not available"

@tool("GetActualDepartureDate")
def getActualDepartureDate(train_status):
    try:
        actual_departure_date = train_status['body']['stations'][0]['actual_departure_date']
        return actual_departure_date
    except KeyError:
        return "Data not available"

@tool("GetActualDepartureTime")
def getActualDepartureTime(train_status):
    try:
        actual_departure_time = train_status['body']['stations'][0]['actual_departure_time']
        return actual_departure_time
    except KeyError:
        return "Data not available"

@tool("GetExpectedPlatform")
def getExpectedPlatform(train_status):
    try:
        expected_platform = train_status['body']['stations'][0]['expected_platform']
        return expected_platform
    except KeyError:
        return "Data not available"