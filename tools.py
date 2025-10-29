from langchain.tools import tool 
from datetime import date
import http.client
import json
import streamlit as st
import requests
import wikipediaapi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def _get_secret(path_keys, env_key):
    try:
        value = st.secrets
        for key in path_keys:
            value = value[key]
        return value
    except Exception:
        import os
        return os.getenv(env_key)

def fetching(): 
    rapid_api_key = _get_secret(['api_keys', 'RAPID_API_KEY'], 'RAPID_API_KEY')
    if not rapid_api_key:
        # Graceful fallback mock when API key is not available
        return {
            "body": {
                "train_status_message": "Mocked status (API key missing)",
                "current_station": "N/A",
                "stations": []
            }
        }
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
    return json_data

@tool("Get current date")
def getCurrentDate():
    """Get the current date in DD/MM/YYYY format for use in formal letters."""
    try:
        today = date.today()
        formatted_date = today.strftime("%d/%m/%Y")
        return formatted_date
    except Exception as e:
        return "27/10/2025"  # Fallback date

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

    # Accept both string and dict inputs from tool callers
    if isinstance(query, dict):
        q = query.get('title') or query.get('q') or str(query)
    else:
        q = str(query)

    payload = json.dumps({"q": q, "num": top_result_to_return, "gl": "in"})
    serper_api_key = _get_secret(['api_keys', 'SERPER_API_KEY'], 'SERPER_API_KEY')
    if not serper_api_key:
        return "Internet search unavailable: missing SERPER_API_KEY."
    headers = {
        'X-API-KEY': serper_api_key,
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





