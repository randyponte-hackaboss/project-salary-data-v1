import numpy as np
import pandas as pd
import re
from datetime import datetime, timedelta

skills = pd.read_csv("Competencias Técnicas-Todas las competencias técnicas.csv")["Competencia"]

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



#####################

# Transforma la fecha de "createdTime" a datetime. Columna creada en Airtable.
# df2["airtable_createdTime"] = df2["airtable_createdTime"].apply(lambda x : datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.000Z") if " " not in x else x)
# Sobreescribe "date_posted", restando la fecha de creación con el timedelta de "date_posted".
# df2["date_posted"] = (df2["airtable_createdTime"] - df2["date_posted"]).apply(lambda x : x.date())

