def getDatosPuesto(driver, puesto, provincia):
    driver.get('https://salarios.infojobs.net/' + puesto + '/' + provincia['value'])

    if "No hemos encontrado resultados. Elige entre los puestos/provincias sugeridos." in driver.page_source:
        return None
    else:
        rango_bajo = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[1]/h4')
        rango_alto = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[3]/h4')
        promedio = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/h4')
        return [float(rango_bajo.text.replace("€", "").replace(".", "")),
                float(rango_alto.text.replace("€", "").replace(".", "")),
                float(promedio.text.replace("€", "").replace(".", ""))]
