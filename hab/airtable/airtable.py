import pandas as pd
import requests
# from time import sleep
import json

class AirtableHAB():
    
    def __init__(self, table_name):

        """
        Tables: Spain, LATAM 001, LATAM 002, LATAM 003, LATAM 004, LATAM 000
        """

        with open(file = "C:\\Users\\danie\\anaconda3\\Lib\\site-packages\\hab\\airtable\\tables.json", mode = "r") as file:
            tables = json.load(file)

        self.table_name = table_name
        self.airtable_oauth = {"base_id"  : "appU0CLDju62P5dKe",
                               "table_id" : get_table_id(table_name = self.table_name, tables = tables),
                               "token"    : "keyvnQcc1FFCaFsDR"}
        
        self.token = self.airtable_oauth["token"]
        self.base_id = self.airtable_oauth["base_id"]
        self.table_id = self.airtable_oauth["table_id"]

        self.endpoint = f"https://api.airtable.com/v0/{self.base_id}/{self.table_id}"


        self.headers = {"Authorization" : f"Bearer {self.token}",
                        "Content-Type"  : "application/json"}

        self.single_category_columns = ["company_name", "location", "source", "country", "contract_type", "remote_work"]
        self.multiple_category_columns = ["tech_skills"]

        self.table_info = tables[self.table_id]

        # with open(file = r"C:\Users\danie\anaconda3\Lib\site-packages\hab\airtable\tables.json", mode = "r") as file:
        #     self.table_info = json.load(file)[self.table_id]
        
    def airtable_post(self, df):

        datos_json = [{"fields" : df.iloc[i, :].to_dict()} for i in range(df.shape[0])]

        for i in range(0, df.shape[0], 10):

            data = {"records" : datos_json[i : i + 10],
                    "typecast" : True} # Add "typcast" : True to allow new elements in category columns

            response = requests.post(url = self.endpoint, json = data, headers = self.headers) # POST

            print(response.status_code)
            if response.status_code != 200:
                print(response.json())

        print(f"{len(datos_json)} added to {self.table_name}")  
        
    def airtable_get(self):

        params = {"offset" : None}

        df_airtable = pd.DataFrame()

        while params.get("offset") != None or df_airtable.shape[0] == 0:

            response = requests.get(url = self.endpoint, headers = self.headers, params = params)

            params["offset"] = response.json().get("offset")

            df_airtable = pd.concat(objs = [df_airtable, pd.json_normalize(response.json()["records"])],
                                    ignore_index = True)

            # sleep(0.5)
            
        df_airtable.columns = [x.split(".")[-1] if len(x.split(".")) > 1 else f"airtable_{x}" for x in df_airtable.columns]

        return df_airtable
    
    # def fill_na(self, df):

    #     for column in ["country", "remote_work", "contract_type"]:
        
    #         try:
    #             df[column] = df[column].fillna("N/A")
    #             df[column] = df[column].astype(str)
    #         except:
    #             pass

    #     df = df.fillna("")
        
    #     df = df.rename(mapper = self.table_info["field_ids"], axis = 1)
        
    #     return df
    

def get_table_id(table_name, tables):

    for key, value in tables.items():

        if value["table_name"] == table_name:
            
            return key
        
    else:
        return f"No table_name: {table_name}"



