# PIPELINE

import pandas as pd
from libraries.preprocess import preprocess
    
funciones = [preprocess.date_posted,
             preprocess.job_id,
             preprocess.title,
             preprocess.source,
             preprocess.location,
             preprocess.contract_type,
             preprocess.created_date,
             preprocess.update_date_posted,
             preprocess.tech_skills,
             preprocess.especialidad_perfil, 
             preprocess.years_experience,
             preprocess.remote_work,
             preprocess.update_contract_type,
             preprocess.update_location_latam_spain]

def pipeline(funciones, df):
    for funcion in funciones:
        print(funcion)
        funcion(df)
            
    return df[["job_id", "country", "experience", "experience_level", "description", "job_specialization",
               "job_profile", "remote_work", "tech_skills", "title", "company_name", "location", "source",
               "date_posted", "contract_type"]]