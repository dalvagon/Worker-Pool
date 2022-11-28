import requests
from pprint import pprint


def get_countries():
    """Returns a list of all countries in the world"""
    API_URL = "https://restcountries.com/v3.1/all"
    response = requests.get(API_URL)
    content = response.json()
    countries = [country["name"]["common"] for country in content]

    return countries
