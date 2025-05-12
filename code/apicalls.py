import requests

# Put your CENT Ischool IoT Portal API KEY here.
APIKEY = "cab8afd61a152b2e03c25247"

def get_google_place_details(google_place_id: str) -> dict:
    headers = { 'X-API-KEY': APIKEY }
    payload = { 'place_id': google_place_id }
    endpoint = "https://cent.ischool-iot.net/api/google/places/details"
    res = requests.get(endpoint, headers=headers, params=payload)
    res.raise_for_status()
    return res.json()

def get_azure_sentiment(text: str) -> dict:
    headers = { 'X-API-KEY': APIKEY }
    body = { "text": text }
    endpoint = "https://cent.ischool-iot.net/api/azure/sentiment"
    res = requests.post(endpoint, headers=headers, data=body)
    res.raise_for_status()
    return res.json()

def get_azure_key_phrase_extraction(text: str) -> dict:
    headers = { 'X-API-KEY': APIKEY }
    body = { "text": text }
    endpoint = "https://cent.ischool-iot.net/api/azure/keyphrasextraction"
    res = requests.post(endpoint, headers=headers, data=body)
    res.raise_for_status()
    return res.json()

def get_azure_named_entity_recognition(text: str) -> dict:
    headers = { 'X-API-KEY': APIKEY }
    body = { "text": text }
    endpoint = "https://cent.ischool-iot.net/api/azure/entityrecognition"
    res = requests.post(endpoint, headers=headers, data=body)
    res.raise_for_status()
    return res.json()


def geocode(place:str) -> dict:
    '''
    Given a place name, return the latitude and longitude of the place.
    Written for example_etl.py
    '''
    header = { 'X-API-KEY': APIKEY }
    params = { 'location': place }
    url = "https://cent.ischool-iot.net/api/google/geocode"
    response = requests.get(url, headers=header, params=params)
    response.raise_for_status()
    return response.json()  # Return the JSON response as a dictionary


def get_weather(lat: float, lon: float) -> dict:
    '''
    Given a latitude and longitude, return the current weather at that location.
    written for example_etl.py
    '''
    header = { 'X-API-KEY': APIKEY }
    params = { 'lat': lat, 'lon': lon, 'units': 'imperial' }
    url = "https://cent.ischool-iot.net/api/weather/current"
    response = requests.get(url, headers=header, params=params)
    response.raise_for_status()
    return response.json()  # Return the JSON response as a dictionary