from unicodedata import normalize
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import re

spanish_stopwords = stopwords.words('spanish')
english_stopwords = stopwords.words('english')
portugues_stopwords = stopwords.words('portuguese')


def normalize_text(text, remove_stop_words=False):
    text = text.lower()
    text = normalize('NFKD', text).encode('ascii','ignore').decode().strip()

    if remove_stop_words:
        text = remove_stopwords(text)

    return text

def remove_punctuation(text):
    return re.sub("\s\s+", " ", text.replace(".", "").replace("\n", " ").replace("\t", "").replace("!", "").replace(",", "").replace(":", "").replace("¿", ""))

def remove_stopwords(text):
    for language in ["spanish", "english", "portuguese"]:
        text = text.split()
        text = " ".join([word for word in text if word not in set(stopwords.words(language))])

    return text

def join_contexts(contexts:list):
    return " ".join([" ".join(context) for context in contexts])

def normalize_currency(currency):
    if currency == "Peso mexicano (MXN)":
        return "MXN"
    
    if currency == "Peso chileno (CLP)":
        return "CLP"
    
    if currency == "Not provided":
        return 0
    
    if currency == "Peso colombiano (COP)" or currency=="Colombian pesos":
        return "COP"
    
    if currency == "Euros (EUR)" or currency=="euros":
        return "EUR"
    
    if currency == "Guatemalan Quetzales" or currency == "Quetzal guatemalteco (GTQ)":
        return "GTQ"
    
    if currency == "Peso dominicano (DOP)" or currency == "Dominican Pesos":
        return "DOP"
    
    if currency == "Costa Rican colones" or currency == "Colones costarricenses (CRC)":
        return "CRC"
    
    if currency == "Dólares estadounidenses (USD)":
        return "USD"
    
    if currency == "Moneda local":
        return 0

    if currency == "Peso argentino (ARS)" or currency == "Argentinian Pesos":
        return "ARS"
    
    return currency