import numpy as np
import pandas as pd
from datetime import datetime
from time import sleep
from tqdm.auto import tqdm
import pickle as pkl
from pprint import pprint
import requests
import os
import math
import json

from libraries.serpapi import serpapi
from libraries.preprocess import preprocess
from libraries.preprocess import pipeline
from libraries.preprocess import airtable
from machine_learning_model.src.textprocessing.preprocess import normalize_text, remove_punctuation

### EXTRACCIÓN ###

# Cargamos los puestos y nuestra API_KEY
today = datetime.now().strftime("%Y-%m-%d")
    
api_key = str(input("Introduce tu API_KEY de SerpApi: "))

lista_puestos = pd.read_excel("data/lista_puestos.xlsx", header = None)
lista_puestos.columns = ["jobs"]
lista_puestos = lista_puestos["jobs"].tolist()

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
    
    for q in puestos: # Modificar lista de puestos según país/países de preferencia.

        try:
            
            for pagination in range(100):
                
                print(f"{q:60}{pagination}")

                q_params = {"q"             : q,
                            "api_key"       : api_key,
                            "location"      : country.title(),
                            "start"         : pagination*10,
                            "chips"         : "date_posted:3days" # Ofertas de empleo de hace 3 días hasta hoy
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
                 
df = df.drop_duplicates(subset = "job_id").reset_index(drop = True) # Eliminamos duplicados si existen en "job_id"
df = df.drop_duplicates(subset = "description").reset_index(drop = True) # Eliminamos duplicados por descripción de oferta
df["date_posted"] = datetime.strptime(today, "%Y-%m-%d").date()

df.to_csv(f"data/extracted/extraction_{today}_{pais}.csv", index = False)


### PROCESAMIENTO ###

df = pipeline.pipeline(funciones = pipeline.funciones, 
                       df = df)

df = df.rename(columns = {"experience_level" : "experience_levels",
                          "job_specialization" : "Especialidad",
                          "job_profile" : "Perfil"})

df.to_csv(f"data/cleaned/{pais}_cleaned_data_{today}.csv", index = False)

### SUBIDA AIRTABLE ###

airtable_key = str(input("Introduce tu API_KEY de airtable: "))
base = str(input("Introduce la base de la tabla destino: "))
table = str(input("Introduce la tabla destino: "))

airtable.airtable_post_spain(df = df, 
                             airtable_key = airtable_key, 
                             base = base, 
                             table = table)

### EXTRACCIÓN DE SALARIOS ###

df[["salary_min_form", "salary_max_form", "currency_form", "time_lapse_form"]] = ""

# Función extracción

def extract_salary(description, job_id, location):
    response = requests.post('http://localhost:3000/predict',
                             data = json.dumps({"description" : description,
                                                "jobid" : job_id,
                                                "location" : location
                                               }),
                             headers = {"Content-Type" : "application/json"})

    if response.status_code == 200:
        return response.json()
    
    return {'max': 0, 'min': 0, 'error_status_code': response.status_code}

# Código para enviar tokens a GPT y que extraiga la información que necesitamos

salary_info = list()
total_tokens = 0
accumulate_cost = 0
progress_steps = math.ceil(df.shape[0]*0.15)

for index, row in tqdm(df.iterrows(), total = df.shape[0]):
    
    try:
        
        salary_output = extract_salary(description = row.description, job_id = row.job_id, location = row.country)
        sent_tokens = salary_output["token_count_sent_chat_gpt"]
        total_tokens += sent_tokens

        cost = float(salary_output["cost"])
        accumulate_cost += cost

        orignal_description_tokens = len(row.description.split(" "))
        reduce_description_len = len(salary_output["reduce_description"].split(" "))
        ratio_sent_original_description = reduce_description_len/orignal_description_tokens

        salary_info.append((row.job_id, salary_output["reduce_description"], salary_output["min"], salary_output["max"], salary_output["currency"], salary_output["time_lapse"], salary_output["source"], sent_tokens, orignal_description_tokens, ratio_sent_original_description, cost))

        if (index%progress_steps) == 0:
            
            print(f"[output salary: {salary_output}]")
            print("[------- Full Description -------]")
            print(row.description)
            print("[------- Reduce description -------]")
            print(salary_output["reduce_description"])
            print(f"==== Tokens sent for this JD:{sent_tokens} - Total sent tokens: {total_tokens} - tokens in complete description:{orignal_description_tokens} = Ratio sent/original description so far:{ratio_sent_original_description} | Cost for this JD:{cost} - Total cost so far: {accumulate_cost} ====")

    except Exception as e:
        
        print(f"error: {e}")

print(f"estimated_cost: {accumulate_cost} per: {df.shape[0]} jobs description | Total sent tokens: {total_tokens}")

salary_df = pd.DataFrame(salary_info,
                         columns=[
                                    "job_id",
                                    "reduce_description",
                                    "salary_min_gpt",
                                    "salary_max_gpt",
                                    "currency_gpt",
                                    "time_lapse_gpt",
                                    "source",
                                    "token_count_sent_chat_gpt",
                                    "token_count_original_description",
                                    "token_rate_sent_original_description",
                                    "gpt_cost"
                                ])

jobs_with_salary = pd.merge(df, salary_df, on = "job_id", how = "left") # Agregamos datos faltantes al nuevo salary_df

# Revisamos cuantos salarios ha extraido y su porcentaje

all_jobs_count = jobs_with_salary.shape[0]
jobs_with_salary_count = jobs_with_salary[jobs_with_salary[f"salary_min_gpt"] > 0].shape[0]

print(f"Salary jobs count: {all_jobs_count} | {jobs_with_salary_count} - jobs with salary {round(jobs_with_salary_count/all_jobs_count, 3)}%")

sleep(5)

# Reajustamos algún que otro nombre en las columnas de datos y procedemos a guardar el archivo final

jobs_with_salary = jobs_with_salary[["job_id", "country", "experience", "experience_levels", "description", "email",
                                     "Especialidad", "Perfil", "remote_work", "tech_skills", "title", "company_name",
                                     "location", "source", "date_posted", "contract_type", "salary_min_gpt",
                                     "salary_max_gpt", "currency_gpt", "time_lapse_gpt"]]

jobs_with_salary = jobs_with_salary.rename(columns = {"salary_min_gpt" : "salary_min",
                                                      "salary_max_gpt" : "salary_max",
                                                      "currency_gpt" : "currency",
                                                      "time_lapse_gpt" : "time_lapse"})

jobs_with_salary["currency"].replace(" ", np.nan, inplace = True)
jobs_with_salary["time_lapse"].replace(" ", np.nan, inplace = True)

jobs_with_salary.to_csv(f"data/with_salaries/{pais}_cleaned_data_{today}_with_salaries.csv", index = False)