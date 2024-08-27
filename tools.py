from langchain.tools import tool 
from datetime import date
import http.client
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


@tool("Get train status")
def getTrainStatus(train_number):
    """Fetch the real-time status of a specific train."""
    conn = http.client.HTTPSConnection("indian-railway-irctc.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': rapid_api_key,
        'x-rapidapi-host': "indian-railway-irctc.p.rapidapi.com",
        'x-rapid-api': "rapid-api-database"
    }
    conn.request("GET", "/api/trains/v1/train/status?departure_date=20240827&isH5=true&client=web&train_number=11040", headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))