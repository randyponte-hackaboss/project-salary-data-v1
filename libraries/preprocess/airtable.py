import numpy as np
import pandas as pd
from time import sleep

import requests
from bs4 import BeautifulSoup

from pprint import pprint

# Airtable post function        
def airtable_post_spain(df):

    airtable_oauth = {"base_id"  : "AIRTABLE_BASE",
                      "table_id" : "AIRTABLE_TABLE",
                      "token"    : "AIRTABLE_KEY"}

    token = airtable_oauth["token"]
    base_id = airtable_oauth["base_id"]
    table_id = airtable_oauth["table_id"]

    endpoint = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    headers = {"Authorization" : f"Bearer {token}",
               "Content-Type"  : "application/json"}
    
    # Fixes to extract lists from strings created on previous steps
    def fix_eval(string):
        
        try:
            return list(eval(string))
        
        except:
            return np.nan
        
    df["Especialidad"] = df["Especialidad"].apply(lambda x : fix_eval(x))
    df["Perfil"] = df["Perfil"].apply(lambda x : fix_eval(x))
    df["remote_work"] = df["remote_work"].apply(lambda x : fix_eval(x))
    df["tech_skills"] = df["tech_skills"].apply(lambda x : fix_eval(x))
    df["location"] = df["location"].apply(lambda x : fix_eval(x))

    df = df.replace(np.nan, None)

    data = [{"fields" : df.iloc[i, :].to_dict()} for i in range(df.shape[0])]

    for i in range(0, len(data), 10):
        
        # Add "typecast" : True to allow new elements in category columns
        data_upload = {"records" : data[i : i + 10],
                       "typecast" : True}

        response = requests.post(url = endpoint, json = data_upload, headers = headers) # POST

        print(response.status_code)
        
        if response.status_code != 200:
            print(response.json())