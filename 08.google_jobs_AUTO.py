import numpy as np
import pandas as pd
from datetime import datetime
from time import sleep
import pickle as pkl
from pprint import pprint
import requests

from libraries.serpapi import serpapi
from libraries.preprocess import preprocess
from libraries.preprocess import pipeline
from libraries.preprocess import airtable

### EXTRACCIÓN ###

# Cargamos los puestos y nuestra API_KEY
today = datetime.now().strftime("%Y-%m-%d")
    
api_key = str(input("Introduce tu API_KEY de SerpApi: "))

lista_puestos = pd.read_excel("data/lista_puestos.xlsx", header = None)
lista_puestos.columns = ["jobs"]

with open("data/lista_puestos_ingles.txt", "r") as file:
    lista_puestos_ingles = file.read()
    
lista_puestos_ingles = lista_puestos_ingles.split("\n")

lista_puestos_ingles = [x for x in [x.replace("Developer", "") for x in lista_puestos_ingles] if len(x.split()) > 1]

# Ajustamos España como país de búsqueda
spain = [[".es", "Spain"]]

# Ajustamos Latino-américa como países de búsqueda
latam = [["com.ar", "Argentina"]         ,
         ["com.bo", "Bolivia"]           ,
         ["com.br", "Brazil"]            ,
         ["cl", "Chile"]             ,
         ["com.co", "Colombia"]          ,
         ["co.cr", "Costa Rica"]        ,
         ["com.cu", "Cuba"]              ,
         ["com.do", "Dominican Republic"],
         ["com.ec", "Ecuador"]           ,
         ["com.sv", "El Salvador"]       ,
         ["com.gt", "Guatemala"]         ,
         ["hn", "Honduras"]          ,
         ["com.mx", "Mexico"]            ,
         ["com.ni", "Nicaragua"]         ,
         ["com.pa", "Panama"]            ,
         ["com.py", "Paraguay"]          ,
         ["com.pe", "Peru"]              ,
         ["com.pr", "Puerto Rico"]       ,
         ["com.uy", "Uruguay"]]

paises = str(input("¿Dónde quieres hacer búsquedas de empleo? Para España: spain, para Latinoamérica: latam "))

if paises == "spain":
    paises = spain
    puestos = lista_puestos
    pais = "spain"

elif paises == "latam":
    paises = latam
    puestos = lista_puestos_ingles
    pais = "latam"

df = pd.DataFrame()

for abr, country in paises:
    
    for q in puestos:

        try:
            
            for pagination in range(100):
                
                print(f"{q:60}{pagination}")

                q_params = {"q"             : q,
                            "api_key"       : api_key,
                            "location"      : country.title(),
                            "start"         : pagination*10
                            }

                response = serpapi.job_search(**q_params)


                if ("error" in response) or (response.get("jobs_results") == None) or (len(response.get("jobs_results")) < 10):
                    break

                df_response = pd.json_normalize(response["jobs_results"])

                df_response.columns = [x.split(".")[0] if len(x.split(".")) == 1 else x.split(".")[-1] for x in df_response.columns]

                df_response["country_search"] = country.title()
                
                df = pd.concat(objs = [df, df_response], ignore_index = True)
                
        except:
            
            print(f"Error {q} ***************************************************************")
                 
df = df.drop_duplicates(subset = "job_id").reset_index(drop = True)
df["date_posted"] = datetime.strptime(today, "%Y-%m-%d").date()

df.to_csv(f"data/extraction_{today}_{pais}.csv", index = False)


### PROCESAMIENTO ###

df = pipeline.pipeline(funciones = pipeline.funciones, 
                       df = df)

df = df.rename(columns = {"experience_level" : "experience_levels",
                          "job_specialization" : "Especialidad",
                          "job_profile" : "Perfil"})

df.to_csv(f"data/{pais}_cleaned_data_{today}.csv", index = False)

### SUBIDA AIRTABLE ###

airtable_key = str(input("Introduce tu API_KEY de airtable: "))
base = str(input("Introduce la base de la tabla destino: "))
table = str(input("Introduce la tabla destino: "))

airtable.airtable_post_spain(df = df, 
                             airtable_key = airtable_key, 
                             base = base, 
                             table = table)