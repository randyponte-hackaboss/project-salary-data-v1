import json
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from funciones import getDatosPuesto
from vars import PUESTOS, PROVINCIAS

options = Options()
options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
+"AppleWebKit/537.36 (KHTML, like Gecko)"
+"Chrome/87.0.4280.141 Safari/537.36")

DRIVER_PATH = './chromedriver'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

data = {"fields": {}}

for puesto in PUESTOS:
    for provincia in PROVINCIAS:
            # SI NO EXISTE FILA PARA PUESTO Y PROVINCIA EN AIRTABLE

            headers = {"Authorization": "Bearer keyhQTL5g0GiqpnYD"}
            filter = 'AND(Puesto="' + puesto + '",Provincia="' + provincia["label"] + '")'
            url = "https://api.airtable.com/v0/appcDODw54oP73Oo3/Datos%20Salarios%20Desarrollador%20Software%202?filterByFormula=" + filter
            jsonResponse = requests.get(url=url, headers=headers)

            response = json.loads(jsonResponse.text)

            if (len(response['records'])) == 0:
                print("No se ha encontrado resultado en Airtable para puesto " + puesto + " en provincia " + provincia["label"])
                print("Cotejando con infojobs")
                datosPuesto = getDatosPuesto(driver, puesto, provincia)
                if datosPuesto:
                    data['fields']['Puesto'] = puesto
                    data['fields']['Provincia'] = provincia['label']
                    data['fields']['Rango Bajo'] = datosPuesto[0]
                    data['fields']['Rango Alto'] = datosPuesto[1]
                    data['fields']['Promedio']= datosPuesto[2]
                    
                headers = {"Content-Type" : "application/json",
                           "Authorization": "Bearer keyhQTL5g0GiqpnYD"}
                url = "https://api.airtable.com/v0/appcDODw54oP73Oo3/Datos%20Salarios%20Desarrollador%20Software%202"
                response = requests.post(url = url, data=json.dumps(data), headers=headers)
            else:
                print("SKIP. Se ha encontrado resultado en Airtable para puesto " + puesto + " en provincia " + provincia["label"])

driver.quit()
