from langchain.tools import tool 
from datetime import date
import http.client
import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()
rapid_api_key = os.getenv('RAPID_API_KEY')

def fetching(): 
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
    print(json_data)
    return json_data

@tool("Get current date")
def getCurrentDate():
    """used to fetch the current date in a formatted manner."""
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    return d

@tool("Get train status")
def getTrainStatus(train_number):
    """Fetch the real-time status of a specific train."""
    json_data = fetching()
    return f"status: {json_data['body']['train_status_message']}, Current_station: {json_data['body']['current_station']}"


@tool("Get station information")
def getStationInfo(train_number, station_code):
    """Fetch information related to a specific station/stop of a train."""
    json_data = fetching()
    for item in json_data['body']['stations']: 
        if(item['stationCode'] == station_code): 
            return item 
    
    return "We are unable to fetch the data needed."


@tool("Search the internet")
def search_internet(query):
    """Useful to search the internet about a a given topic and return relevant results"""
    print("Searching the internet...")
    top_result_to_return = 5
    url = "https://google.serper.dev/search"
    payload = json.dumps(
        {"q": query, "num": top_result_to_return, "tbm": "nws"})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
        # check if there is an organic key
    if 'organic' not in response.json():
        return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
    else:
        results = response.json()['organic']
        string = []
        print("Results:", results[:top_result_to_return])
        for result in results[:top_result_to_return]:
            try:
                    # Attempt to extract the date
                date = result.get('date', 'Date not available')
                string.append('\n'.join([
                    f"Title: {result['title']}",
                    f"Link: {result['link']}",
                    f"Date: {date}",  # Include the date in the output
                    f"Snippet: {result['snippet']}",
                    "\n-----------------"
                ]))
            except KeyError:
                next

        return '\n'.join(string)