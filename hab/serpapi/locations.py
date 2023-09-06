import pandas as pd
import json

def read_locations():
    with open(file = "locations.json", mode = "r", encoding = "UTF-8") as file:
        locations = json.load(file)

    return locations

def all_locations():
    locations = read_locations()

    df = pd.json_normalize(locations)

    return df 

def country_locations(country_code = 'es'):

    """
    Params:
    country_code: required: (string): default: 'es'
    """

    df = all_locations()

    df = df[df["country_code"] == country_code.upper()].reset_index(drop = True)

    return df