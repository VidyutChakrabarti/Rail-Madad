from langchain.tools import tool 
from datetime import date
import http.client
import json
import streamlit as st
import requests
import wikipediaapi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


rapid_api_key = st.secrets['api_keys']['RAPID_API_KEY']

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
    #print(json_data)
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
    
    return "Train doesn't stop at the station specified."


@tool("Search the internet")
def search_internet(query):
    """Useful to search the internet about a a given topic and return relevant results"""
    top_result_to_return = 5
    url = "https://google.serper.dev/search"
    payload = json.dumps(
        {"q": query['title'], "num": top_result_to_return, "gl": "in"})
    headers = {
        'X-API-KEY': st.secrets['api_keys']['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if 'organic' not in response.json():
        return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
    else:
        results = response.json()['organic']
        string = []
        print(results)
        for result in results[:top_result_to_return]:
            try:
                string.append(' '.join([
                    f"Title: {result['title']}",
                    f"Snippet: {result['snippet']}",
                ]))
            except KeyError:
                next

        return '\n'.join(string)
    
@tool("Wikipedia Tool")
def get_wikipedia_summary(page_title):
    """Fetch the summary of a Wikipedia page."""
    wiki_wiki = wikipediaapi.Wikipedia('en') 
    page = wiki_wiki.page(page_title)
    if page.exists():
        return page.summary
    else:
        return "Page not found."

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    if sentiment['compound'] > 0:
        sentiment_label = 'Positive'
    elif sentiment['compound'] < 0:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'
    
    return sentiment_label, sentiment['compound']

@tool("Get department contact information")
def get_department_contact(department_name):
    """Retrieve contact information for a specific department."""

    contacts = {
        "Customer Service": "customer.service@railways.com",
        "Technical Support": "tech.support@railways.com",
        "Maintenance": "maintenance@railways.com"
    }
    return contacts.get(department_name, "Department not found.")





