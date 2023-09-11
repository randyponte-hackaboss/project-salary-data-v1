import numpy as np
import pandas as pd
import re
from datetime import datetime, timedelta
import json
import os

skills = pd.read_csv("data/Competencias Técnicas-Todas las competencias técnicas.csv")["Competencia"]

datetime_object = datetime(year = 1970, month = 1, day = 1).date()

# Contract Type
map_contract_type = {"Tiempo completo"   : "Full-time",
                     "A tiempo completo" : "Full-time",
                     "A tiempo parcial"  : "Part-time",
                     "Prácticas"         : "Internship",
                     "Pasantía"          : "Internship",
                     "Medio tiempo"      : "Part-time",
                     "Contratista"       : "Contractor",
                     "Pekerjaan tetap"   : "Full-time",
                     "Полная занятость"  : "Full-time",
                     "Стажировка"        : "Internship",
                     "Full-time"         : "Full-time",
                     "Full-Time"         : "Full-time",
                     "Fulltime"          : "Full-Time",
                     "Part-time"         : "Part-time",
                     "Part-Time"         : "Part-time",
                     "Parttime"          : "Part-time",
                     "Contractor"        : "Contractor",
                     "دوام كامل"        : "Full-Time",
                     "正職員工"           : "Full-Time",
                     "Полная занятость"  : "Full-Time",
                     "フルタイム"         : "Full-Time",
                     "متعاقد"           : "Contractor",
                     "دوام جزئي"        : "Part-Time"}

# Creates dataframe from .json files
archives = os.listdir("C:\\Users\\germa\\Desktop\\HACK A BOSS\\proyecto_job-salary\\data\\data_1") # Change PATH to your .json files' container, always use "\\" instead of  "\"

def dataframe(archives):

    # Create dataframe with all .json files' content
    dates = list()

    df = pd.DataFrame()

    for json_ in archives:
        
        with open(json_, "br") as file:
            data = json.load(file) # Using pickle throws an error that json fix.
            
        date = datetime.strptime(data["search_metadata"]["created_at"], "%Y-%m-%d %H:%M:%S UTC").date()

        try:

            df_ = pd.json_normalize(data["jobs_results"])

            for i in range(df_.shape[0]):

                dates.append(date)

            df = pd.concat([df, df_], ignore_index = True)

        except:
            pass

        return df, dates

# Creating some data columns and cleaning functions for each column in the dataframe
def data_columns(df, dates):

    # Create "date_posted"
    df["date_posted"] = dates

    # Eliminate duplicates
    df = df.drop_duplicates("job_id").reset_index(drop = True) 

    # Clean "via"
    for i in range(len(df["via"])):
        
        # Due to some NoneType values, use try / except
        try:
            df.loc[i, "via"] = clean_source(df.loc[i, "via"]) # Each row
            
        except:
            df.loc[i, "via"] = np.nan
        
    # Clean "location"
    df["location"] = df["location"].apply(lambda x : clean_location(x))

    # Clean "contract_type"
    df["detected_extensions.schedule_type"] = df["detected_extensions.schedule_type"].apply(lambda x : clean_contract_type(x))

    # Clean "created_date"
    df["detected_extensions.posted_at"] = df["detected_extensions.posted_at"].apply(lambda x : transform_date(x))

    df["date_posted"] = [get_date(x, y) for x, y in df[["date_posted", "detected_extensions.posted_at"]].values]

    # Create "tech_skills"
    for i in range(len(df["description"])):
        
        # Due to some NoneType values, use try / except
        try:
            df.loc[i, "tech_skills"] = get_skills(df.loc[i, "description"]) # Each row
            
        except:
            df.loc[i, "tech_skills"] = np.nan

    return df

def clean_contract_type(string):
    
    if type(string) != str:
        return None

    return map_contract_type[string.capitalize()] if string.capitalize() in map_clean_source.keys() else string

#####################

# Source

map_clean_source = {"via "         : "",
                    "a través de " : ""}

def clean_source(string):
    
    for key, value in map_clean_source.items():
        if string.startswith(key):
            string = string.replace(key, value)

    return string

#####################

# Country

map_country_name = {"España" : "Spain",
                    "Испания" : "Spain"}

def get_country(location):
    
    """Return the country of a location."""

    if type(location) != str:
        return "N/A"

    return map_country_name[location] if location.title() in map_country_name else location.title()

#####################

# Location

def clean_location(string):

    if type(string) != str:

        return string

    string = clean_regular_brackets(string.strip())

    return string

#####################

# General

def clean_regular_brackets(string):

    pattern = r"\([^()]*\)"

    string = re.sub(pattern, "", string)

    return string.strip()

def clean_column_names(df):
    df = df.rename(mapper  = {"via"                               : "source",
                              "posted_at"                         : "date_posted",
                              "schedule_type"                     : "contract_type",
                              "work_from_home"                    : "remote_work",
                              "detected_extensions.schedule_type" : "contract_type"},
                   axis    = 1)
    
    return df

#####################

# Date

def transform_date(string):
    
    if type(string) != str:
        
        return string
    
    # Days - Day - Días - Días
    
    if string.endswith("days ago") or string.endswith("day ago"):
                
        return timedelta(days = int(string.split()[0]))
        
    elif string.endswith("días") or string.endswith("día"):
        
        return timedelta(days = int(string.split()[1]))
    
    # Hours - Hour - Horas - Hora
    
    if string.endswith("hours ago") or string.endswith("hour ago"):
        
        return timedelta(hours = int(string.split()[0]))
    
    elif string.endswith("horas") or string.endswith("hora"):
        
        return timedelta(hours = int(string.split()[1]))
    
    # Minutes - Minute - Minutos - Minuto
    
    if string.endswith("minutes ago") or string.endswith("minute ago"):
        
        return timedelta(minutes = int(string.split()[0]))
    
    elif string.endswith("minutos") or string.endswith("minuto"):
        
        return timedelta(minutes = int(string.split()[1]))
    
    # Seconds - Second - Segundos - Segundo
    
    if string.endswith("seconds ago") or string.endswith("second ago"):
        
        return timedelta(seconds = int(string.split()[0]))
    
    elif string.endswith("segundos") or string.endswith("segundo"):
        
        return timedelta(seconds = int(string.split()[1]))
    
    return np.nan

def get_date(date_1, date_2):

    if type(date_1) != type(datetime_object) or type(date_2) != pd._libs.tslibs.timedeltas.Timedelta:

        return date_1
    
    return date_1 - date_2

#####################

# Tech Skills

def get_skills(string, skills = skills):
    
    skills = [skill for skill in skills if skill in string.split() and len(string.split()) > 0]
    
    return skills

#####################

# Salary

map_clean_salary = {"hora"   : 8*7*4*12,
                    "día"    : 7*4*12,
                    "semana" : 4*12,
                    "mes"    : 12,
                    "año"    : 1}

def extract_salary(string):
    
    string = string.split()
    
    string = [s for s in string if any([x for x in s if x.isnumeric()])]
        
    return string

def formato_1(text):
    pattern = r"\b(\d{1,3}(?:[\.,]\d{3})*[Kk]-\d{1,3}(?:[\.,]\d{3})*)[Kk]\b"  # Matches salary information in the format "30-40K"
    matches = re.findall(pattern, text)
    return matches

## Formato: "_K"
def formato_2(text):
    pattern = r"\b(\d{1,3}(?:[\.,]\d{3})*K)\b"  # Matches salary information in the format "30K"
    matches = re.findall(pattern, text)
    return matches

# (30K-40K), [30K-40], [30-40K]
def formato_3(text):
    pattern = r"\b(\d{1,3}(?:[\.,]\d{3})*[Kk]?-\d{1,3}(?:[\.,]\d{3})*[Kk]?)\b"  # Matches salary information in formats like "30K-40K", "[30K-40]", or "[30-40K]"
    matches = re.findall(pattern, text)
    return matches

# 300 - 400 €, 300-400€
def formato_4(text):
    pattern = r"\b(\d{1,3}(?:[\.,]\d{3})*\s*-\s*\d{1,3}(?:[\.,]\d{3})*\s*€)\b"  # Matches salary information in formats like "300 - 400 €" or "300-400€"
    matches = re.findall(pattern, text)
    return matches

def clean_k_1000(string1, string2):
    
    if ("k" in string1+string2) or ("K" in string1+string2) or (".000" in string1+string2):
        
        string1 = float(string1.strip("kK.000"))
        string2 = float(string2.strip("kK.000"))
        
        return string1*1000, string2*1000
    
    else:
        return float(string1), float(string2)
    

def all_formatos(string):
    
    resultados = list()
    
    pattern = r"\b(\d{1,3}(?:[\.,]\d{3})*[Kk]-\d{1,3}(?:[\.,]\d{3})*)[Kk]\b"  # Matches salary information in the format "30-40K"
    matches = re.findall(pattern, string)
    
    resultados.extend(matches)
    
    pattern = r"\b(\d{1,3}(?:[\.,]\d{3})*K)\b"  # Matches salary information in the format "30K"
    matches = re.findall(pattern, string)
    
    resultados.extend(matches)
    
    pattern = r"\b(\d{1,3}(?:[\.,]\d{3})*[Kk]?-\d{1,3}(?:[\.,]\d{3})*[Kk]?)\b"  # Matches salary information in formats like "30K-40K", "[30K-40]", or "[30-40K]"
    matches = re.findall(pattern, string)
    
    resultados.extend(matches)
    
    pattern = r"\b(\d{1,3}(?:[\.,]\d{3})*\s*-\s*\d{1,3}(?:[\.,]\d{3})*\s*€)\b"  # Matches salary information in formats like "300 - 400 €" or "300-400€"
    matches = re.findall(pattern, string)
    
    resultados.extend(matches)
    
    resultados = list(set([x for x in resultados if (len(x) > 4) and (not x.startswith("00"))]))
    
    mitad = [x.split("-") for x in resultados]
    
    mitad = list(set([clean_k_1000(x, y) for x, y in mitad]))
    
    mitad = np.array([[x, y] for x, y in mitad if x < y]).flatten()
    
    mitad = [x for x in mitad if x > 100]
    
    return mitad if len(mitad) > 0 else np.nan

# Create a dataframe that contains job information from Spain
def spain(df):

    lista_str_ = ["Spain", "España"]

    for str_ in lista_str_:
        
        if str_ == "Spain":
            df_1 = df[df['location'].str.contains(str_, na = False)]
            
        elif str_ == "España":
            df_2 = df[df['location'].str.contains(str_, na = False)]
            
    df_spain = pd.concat([df_1, df_2])

    return df_spain

#####################

# Transforma la fecha de "createdTime" a datetime. Columna creada en Airtable.
# df2["airtable_createdTime"] = df2["airtable_createdTime"].apply(lambda x : datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.000Z") if " " not in x else x)
# Sobreescribe "date_posted", restando la fecha de creación con el timedelta de "date_posted".
# df2["date_posted"] = (df2["airtable_createdTime"] - df2["date_posted"]).apply(lambda x : x.date())

