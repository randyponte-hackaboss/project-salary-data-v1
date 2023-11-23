import numpy as np
import pandas as pd
import re
from datetime import datetime, timedelta
import json
import os

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

    return prov[0] if prov else np.nan

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

# Fix "company_name"

empresas = pd.read_csv("data/Tabla Maestra de Empresas.csv")

def company_name(string, empresas = empresas):
    
    empresa_final = string.title()
    
    for empresa in empresas["company_name"]:
        
        if empresa == string.lower():
            empresa_final = empresas[empresas["company_name"] == empresa].iloc[0, 1]
        
    return empresa_final or string

#####################

# Tech Skills

skills = pd.read_csv("data/Competencias Técnicas-UPDATE.csv")["Competencia"]

def get_skills(string, skills = skills):
    
    tech_skills = list()
    
    for skill in skills:
        try:
            if skill.lower() in string.lower().split():
                tech_skills.append(skill)
                
        except:
            tech_skills.append(np.nan)
    
    return tech_skills

#####################

# Job Profile & Job Specialization
df_perfil_especialidad = pd.read_csv("data/Tabla Maestra de Etiquetas - Etiquetas Perfil - Especialidad.csv")

list_variantes = df_perfil_especialidad["Variantes (Title)"].unique().tolist()

list_especialidad = df_perfil_especialidad["N2 Especialidad"].dropna().unique().tolist()

dict_perfiles = {v : k for k, v in df_perfil_especialidad[["N1 Perfil", "N2 Especialidad"]].dropna().values}

# Job Specialization
def get_especialidad(string, df_perfil_especialidad):

    list_variantes = df_perfil_especialidad["Variantes (Title)"].dropna().unique().tolist()

    especialidades = list({df_perfil_especialidad[df_perfil_especialidad["Variantes (Title)"] == variante].iloc[0, 2] for variante in list_variantes if variante.lower() in string.lower()})

    return especialidades if especialidades else np.nan

# Job profile
def get_perfil(string, df_perfil_especialidad):

    list_variantes = df_perfil_especialidad["Variantes (Title)"].dropna().unique().tolist()

    perfiles = list({df_perfil_especialidad[df_perfil_especialidad["Variantes (Title)"] == variante].iloc[0, 1] for variante in list_variantes if variante.lower() in string.lower()})

    return perfiles if perfiles else np.nan
    
# Find levels on title first, then on description
niveles = pd.read_csv("data/Tabla Maestra de Niveles.xlsx")

def experience_level(string, niveles = niveles):

    nivel_final = list({niveles[niveles["title"] == nivel].iloc[0, 2] for nivel in niveles["title"] if nivel in string.lower()})
        
    return min(nivel_final) if nivel_final else np.nan

# Find years of experience if levels not in title or description
def find_years_of_experience(string: str):

    try:
        numeros = sorted(re.findall(r"(?P<years>\d+)\-(?P<years_2>\d+) (?P<years_type>años|years|anos|year|año|ano)", string.lower()))[0][1] # Regex to find sentences like: "2-3 years of", "2-3 años de"
        
    except:
        numeros = None
        
    if numeros is None:

        try:
            numeros = sorted(re.findall(r"(?P<years>\d+) \- (?P<years_2>\d+) (?P<years_type>años|years|anos|year|año|ano)", string.lower()))[0][1] # Regex to find sentences like: "2 - 3 years of", "2 - 3 años de"

            return int(numeros) if int(numeros) < 13 else np.nan

        except:
            return np.nan

    elif numeros is not None:

        return int(numeros) if int(numeros) < 13 else np.nan

    else:
        return np.nan
    
# Find years of experience Regex update    
def update_find_years_of_experience(string: str):

    try:
        numeros = sorted(re.findall(r"(?P<years>several|\d+) (?P<years_type>años|years|anos|year|año|ano|or|o)",
                                    string.lower()))[-1][0] # Regex to find sentences like: "5 years of", "5 años de", "several years of"
        
        if numeros == "several":

            numeros = 5
        
    except:
        numeros = None
        
    if numeros is None:

        try:
            numeros = sorted(re.findall(r"(?P<years>\d+)\+ (?P<years_type>años|years|anos|year|año|ano)", string.lower()))[-1][0] # Regex to find sentences like: "5+ years of", "5+ años de"

            return int(numeros) if int(numeros) < 13 else np.nan

        except:
            return np.nan

    elif numeros is not None:

        return int(numeros) if int(numeros) < 13 else np.nan

    else:
        return np.nan

# Dict to convert numbers in words into numbers (int)    
numeros_en_palabras = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce",
                       "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]

numeros_enteros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                   1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

dict_palabras_numeros = dict(zip(numeros_en_palabras, numeros_enteros))
    
def update_2_find_years_of_experience(string: str, dict_palabras_numeros):

    try:
        numeros = sorted(re.findall(r"\((?P<years>\d+)\) (?P<years_type>años|years|anos|year|año|ano)", string.lower()))[-1][0] # Regex to find sentences like: "(5) years of", "(5) años de"
        
    except:
        numeros = None
        
    if numeros is None:

        try:
            numeros = sorted(re.findall(r"(?P<years>one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce+) (?P<years_type>años|years|anos|year|año|ano|or more|o más|o mas)",
                                         string.lower()))[-1][0] # Regex to find sentences like: "five or more years of", "cinco o mas años de", "cinco años", "five years"
            
            numeros = dict_palabras_numeros[numeros]

            return int(numeros) if int(numeros) < 13 else np.nan

        except:
            return np.nan

    elif numeros is not None:

        return int(numeros) if int(numeros) < 13 else np.nan

    else:
        return np.nan
    
# Experience level
def update_experience_level(num):
    
    if not pd.isna(num):
    
        if num < 2:
            return "Junior"
        elif num <= 4:
            return "Semi-Senior"
        elif num <= 8:
            return "Senior"
        else:
            return "Leader"
        
    else:
        return np.nan

# Obtain email from description if exists
def get_email_from_description(string: str):
 
    try:

        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        email = re.findall(pattern, string)[0]

        return str(email) if email else np.nan
    
    except:
        return np.nan
    
def remove_because_in_string(string): # Due to a conflict with some experience levels
    
    return string.replace("because", "") if "because" in string.lower() else string
    
# Calling functions
def especialidad_perfil(df):
    
    df["Especialidad"] = df["description"].apply(lambda x : get_especialidad(x, df_perfil_especialidad = df_perfil_especialidad) if not pd.isna(x) else np.nan)
    df["Especialidad"] = df["Especialidad"].fillna(df["title"].apply(lambda x : get_especialidad(x, df_perfil_especialidad = df_perfil_especialidad) if not pd.isna(x) else np.nan))

    df["Perfil"] = df["description"].apply(lambda x : get_perfil(x, df_perfil_especialidad = df_perfil_especialidad) if not pd.isna(x) else np.nan)
    df["Perfil"] = df["Perfil"].fillna(df["title"].apply(lambda x : get_perfil(x, df_perfil_especialidad = df_perfil_especialidad) if not pd.isna(x) else np.nan))
    # df["job_profile"] = df["job_profile"].fillna(df["title"].apply(lambda x : get_perfil(x, dict_perfiles = dict_perfiles)))

    return df

def years_experience(df):

    df["experience"] = df["description"].apply(lambda x : find_years_of_experience(x))
    df["experience"] = df["experience"].fillna(df["description"].apply(lambda x : update_find_years_of_experience(x)))
    df["experience"] = df["experience"].fillna(df["description"].apply(lambda x : update_2_find_years_of_experience(x, dict_palabras_numeros = dict_palabras_numeros)))

    df["experience_levels"] = df["experience"].apply(lambda x : update_experience_level(x) if not pd.isna(x) else np.nan)
    df["description"] = df["description"].apply(lambda x : remove_because_in_string(x) if not pd.isna(x) else x)
    df["experience_levels"] = df["experience_levels"].fillna(df["title"].apply(lambda x : experience_level(x) if not pd.isna(x) else np.nan))
    df["experience_levels"] = df["experience_levels"].fillna(df["description"].apply(lambda x : experience_level(x) if not pd.isna(x) else np.nan))

    # df["experience"] = df["experience_level"].apply(lambda x : int(df_niveles[df_niveles["title"] == x].iloc[0, 0].strip(" <>")) if not pd.isna(x) else np.nan)
    # df["experience_level"] = df["experience_level"].apply(lambda x : x.title() if not pd.isna(x) else np.nan) # First letter in mayus
    
    return df

def fix_company_name(df):

    df["company_name"] = df["company_name"].apply(lambda x : company_name(x) if not pd.isna(x) else x)

    return df

def email(df):

    df["email"] = df["description"].apply(lambda x : get_email_from_description(x))

    return df                                                  

#####################

# Remote Work
def get_remote_work(string):
    
    resultados = list()
    
    try:

        if "remoto" in string or "REMOTO" in string or "remote work" in string or "Remote Work" in string or "REMOTE WORK" in string or "remote" in string or "REMOTE" in string or "remota" in string or "REMOTA" in string:

            resultados.append("Remoto")

        elif "hibrido" in string or "HIBRIDO" in string or "hybrid" in string or "HYBRID" in string or "híbrido" in string or "HÍBRIDO" in string or "hibrida" in string or "HIBRIDA" in string or "híbrida" in string or "HÍBRIDA" in string:

            resultados.append("Hibrido")

        elif "presencial" in string or "Presencial" in string or "PRESENCIAL" in string or "in-office" in string or "In-Office" in string or "IN-OFFICE" in string or "Oficina" in string or "OFICINA" in string or "oficina" in string:

            resultados.append("Presencial")

        else:
            return np.nan
        
    except:

        return np.nan
        
    return resultados

# Calling function
def remote_work(df):

    df["remote_work"] = df["description"].apply(lambda x : get_remote_work(x))
    df["remote_work"] = df["remote_work"].fillna(df["title"].apply(lambda x : get_remote_work(x) if not pd.isna(x) else np.nan))

    return df

#####################

# Data columns

def date_posted(df):
    # Create "date_posted"
    df["date_posted"] = df["date_posted"].apply(lambda x : pd.to_datetime(x).date())
    
    return df

def normalize_title(df):
    # Normalize punctuation
    df["title"] = df["title"].str.normalize("NFC")

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
    
    df["contract_type"] = df["schedule_type"].apply(lambda x : clean_contract_type(x))
    # df["contract_type"] = df["detected_extensions.schedule_type"].apply(lambda x : clean_contract_type(x))
    
    return df

def created_date(df):
    # Clean "created_date"

    df["posted_at"] = df["posted_at"].apply(lambda x : transform_date(x))
    # df["posted_at"] = df["detected_extensions.posted_at"].apply(lambda x : transform_date(x))
    
    return df

def update_date_posted(df):
    df["date_posted"] = [get_date(x, y) for x, y in df[["date_posted", "posted_at"]].values]
    
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

    df["country"] = df["country_search"]
    # df["country"] = df["location"].apply(lambda x : dict_1.get(x, x))
    
    df["location"] = df["location"].apply(lambda x : last_location_update(x))
        
    return df
    
def tech_skills(df):
    # Create "tech_skills"
    df["tech_skills"] = df["description"].apply(lambda x : get_skills(x))
            
    return df

def fix_eval(string):
        
        try:
            return list(eval(string))
        
        except:
            return np.nan
        
def last_fix(df):
    # Fixes to extract lists from strings created on previous steps
    df["Especialidad"] = df["Especialidad"].apply(lambda x : fix_eval(x))
    df["Perfil"] = df["Perfil"].apply(lambda x : fix_eval(x))
    df["remote_work"] = df["remote_work"].apply(lambda x : fix_eval(x))
    df["tech_skills"] = df["tech_skills"].apply(lambda x : fix_eval(x))
    
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