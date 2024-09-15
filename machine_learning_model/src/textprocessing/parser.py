import re


def return_min_max(response_text):
    if len(response_text["salary"])>0:
        number = re.compile("[0-9]+")
        return [int(value) for value in number.findall(response_text["salary"][0]['salary'].replace(".", ""))]
    
    return [0, 0]
