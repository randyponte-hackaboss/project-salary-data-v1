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
        
        try:
            if string.startswith(key):
                string = string.replace(key, value)
                
        except:
            string = np.nan

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

def string_contains(string, value):

    if value in string:
        return True
        
    return False

def last_location_update(string):
    
    provinces = pd.read_csv("data/world_provinces.csv")["estadonombre"]

    prov = list()

    for province in provinces:
        try:
            if string_contains(string, province):
                prov.append(province)
            
        except:
            prov.append(np.nan)

    return prov

#####################

# General

def clean_regular_brackets(string):

    pattern = r"\([^()]*\)"

    string = re.sub(pattern, "", string)

    return string.strip()

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
    
    tech_skills = list()
    
    for skill in skills:
        try:
            if skill in string.split():
                tech_skills.append(skill)
                
        except:
            tech_skills.append(np.nan)
    
    return tech_skills

#####################

# Job Profile & Job Specialization

df_perfil_especialidad = pd.read_csv("data/StackMinimo - StackTec.csv", skiprows = 2).drop("Unnamed: 0", axis = 1)
list_especialidad = df_perfil_especialidad["N2 Especialidad"].dropna().to_list()

list_especialidad = ["Backend",
                     "Base de datos",
                     "Bases de datos",
                     "APIs",
                     "Mobile",
                     "Frontend Movil",
                     "Frontend Web",
                     "Full Stack",
                     "Integración",
                     "Liferay",
                     "Power BI",
                     "Software Release Engineer",
                     "SRE",
                     "Diseñador Gráfico",
                     "Graphic Designer",
                     "Infraestructura cloud",
                     "Estructuras cloud",
                     "Sistemas Operativos",
                     "Seguridad",
                     "Mantenimiento y Soporte",
                     "Administrador de Base de datos",
                     "Servidores y aplicaciones",
                     "Tester funcional",
                     "Tester automatizada",
                     "SCRUM Master",
                     "Product Owner",
                     "Customer Success",
                     "Gerente de Proyecto",
                     "Analisis de Datos",
                     "Analista de Datos"]

dict_perfiles = {v : k for k, v in df_perfil_especialidad[["N1 Perfil ", "N2 Especialidad"]].dropna().values}

dict_perfiles = {'Backend': 'Desarrollador',
                 'Base de datos': 'Desarrollador',
                 'APIs': 'Desarrollador',
                 'Mobile': 'Desarrollador',
                 'Frontend Movil': 'Desarrollador',
                 'Frontend Web': 'Desarrollador',
                 'Full Stack': 'Desarrollador',
                 'Integración': 'Desarrollador',
                 'Liferay': 'Desarrollador',
                 'Power BI': 'Desarrollador',
                 'Software Release Engineer': 'Devops',
                 'Diseñador Gráfico': 'Diseñador',
                 'Infraestructura cloud': 'Infraestructura',
                 'Sistemas Operativos': 'Infraestructura',
                 'Seguridad': 'Infraestructura',
                 'Mantenimiento y Soporte': 'Infraestructura',
                 'Tester funcional': 'Quality Assurance',
                 'Tester automatizada': 'Quality Assurance',
                 'SCRUM Master': 'Gestión Operativa',
                 'Product Owner': 'Gestión Operativa',
                 'Customer Success': 'Gestión Operativa',
                 'Gerente de Proyecto': 'Gestión Operativa',
                 'Analisis de Datos': 'Especialista'}

# Job Specialization
def get_especialidad(string, list_especialidad):
    
    especialidades = list({especialidad for especialidad in list_especialidad if especialidad.lower() in string.lower()})
    
    return especialidades if especialidades else np.nan

# Job profile
def get_perfil(lista, dict_perfiles):
    
    perfiles = list({v for k, v in dict_perfiles.items() if k in lista})
    
    return perfiles if perfiles else np.nan

# Years Of Experience
def find_years_of_experience(string: str):
    
    list_strings = ["años de", "years of", "years experience", "años experiencia"]
    
    string = string.lower()
    
    years = [string[string.find(s) - 5 : string.find(s) + len(s) + 1] for s in list_strings if string.find(s) != -1]
    
    numeros = [re.findall(r"\d+", y) for y in years]

    numeros = [[int(n) for n in num if 0 < int(n) < 13] for num in numeros]
    
    numeros = [max(num) if num else np.nan for num in numeros]

    return max(numeros) if numeros else np.nan

# Experience Level
def experience_level(num):
    
    if not pd.isna(num):
    
        if num < 2:
            return "Junior"
        elif num <= 4:
            return "Semi-Senior"
        elif num < 8:
            return "Senior"
        else:
            return "Leader"
        
    else:
        return np.nan
    
# Calling functions
def especialidad_perfil(df):

    df["job_specialization"] = df["description"].apply(lambda x : get_especialidad(x, list_especialidad = list_especialidad) if not pd.isna(x) else None)
    df["job_profile"] = df["description"].apply(lambda x : get_perfil(x, dict_perfiles = dict_perfiles) if not pd.isna(x) else None)

    return df

def years_experience(df):

    df["experience"] = df["description"].apply(lambda x : find_years_of_experience(x) if not pd.isna(x) else x)
    df["experience_level"] = df["experience"].apply(lambda x : experience_level(x))

    return df

#####################

# Remote Work

def get_remote_work(string):
    
    resultados = list()
    
    try:
        if "remoto" in string or "remote work" in string or "remote" in string:

            resultados.append("Remoto")

        elif "hibrido" in string or "hybrid" in string or "híbrido" in string:

            resultados.append("Hibrido")

        elif "presencial" in string or "in-office" in string:

            resultados.append("Presencial")

        else:
            return np.nan
        
    except:
        return np.nan
        
    return resultados

# Calling function

def remote_work(df):

    df["remote_work"] = df["description"].apply(lambda x : get_remote_work(x))

    return df

#####################

# Data columns

def date_posted(df, dates):
    # Create "date_posted"
    df["date_posted"] = dates
    
    return df

def job_id(df):
    # Eliminate duplicates
    df = df.drop_duplicates("job_id").reset_index(drop = True) 
    
    return df

def source(df):
    # Clean "via"
    df["source"] = df["via"].apply(lambda x : clean_source(x))
            
    return df

def location(df):
    # Clean "location"
    df["location"] = df["location"].apply(lambda x : clean_location(x))
    
    return df

def contract_type(df):
    # Clean "contract_type"
    df["contract_type"] = df["detected_extensions.schedule_type"].apply(lambda x : clean_contract_type(x))
    
    return df

def created_date(df):
    # Clean "created_date"
    df["detected_extensions.posted_at"] = df["detected_extensions.posted_at"].apply(lambda x : transform_date(x))
    
    return df

def update_date_posted(df):
    df["date_posted"] = [get_date(x, y) for x, y in df[["date_posted", "detected_extensions.posted_at"]].values]
    
    return df

def update_contract_type(df):
    df["contract_type"] = df["contract_type"]\
                          .apply(lambda x : "Full-time" if x == "Tiempo completo" else x)

    return df

def update_location_latam_spain(df):
    
    with open("data/locations_latam.json", "br") as file:
        dict_1 = json.load(file)
        
    with open("data/locations_spain.json", "br") as file:
        dict_2 = json.load(file)
        
    dict_1.update(dict_2)

    df["country"] = df["location"].apply(lambda x : dict_1.get(x, x))
    
    df["location"] = df["location"].apply(lambda x : last_location_update(x))
        
    return df
    
def tech_skills(df):
    # Create "tech_skills"
    df["tech_skills"] = df["description"].apply(lambda x : get_skills(x))
            
    return df

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

#####################

# Transforma la fecha de "createdTime" a datetime. Columna creada en Airtable.
# df2["airtable_createdTime"] = df2["airtable_createdTime"].apply(lambda x : datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.000Z") if " " not in x else x)
# Sobreescribe "date_posted", restando la fecha de creación con el timedelta de "date_posted".
# df2["date_posted"] = (df2["airtable_createdTime"] - df2["date_posted"]).apply(lambda x : x.date())

