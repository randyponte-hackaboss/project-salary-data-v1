from flask import Flask
from flask import request
from src.textprocessing.chat_gpt import chain
from src.textprocessing.regex import get_context_from_numbers_in_text
from src.textprocessing.preprocess import join_contexts, remove_punctuation, normalize_text
# For token counting
from langchain.callbacks import get_openai_callback
from src.cache import load_cache, save_cache
import os
import sys

SIGNAL_WORDS = ["salario", "renta", "sueldo", "retribucion", "salary", "bruto", "liquida"]
NGRAMS = int(os.environ["NGRAMS"]) if "NGRAMS" in os.environ else 3
# I will handle this from the client for now
OVERLAPS_CONTEXT_THRESHOLD = float(os.environ["OVERLAPS_CONTEXT_THRESHOLD"]) if "OVERLAPS_CONTEXT_THRESHOLD" in os.environ else 0.3

print(f"Params NGRAMS: {NGRAMS} | OVERLAP: {OVERLAPS_CONTEXT_THRESHOLD}", file=sys.stdout)

def format_response(salary_min, salary_max, currency, time_lapse, source, token_count_sent_chat_gpt, cost, reduce_description):
    return {
                "min":salary_min, 
                "max":salary_max, 
                "currency":currency, 
                "time_lapse":time_lapse, 
                "source":source,
                "token_count_sent_chat_gpt":token_count_sent_chat_gpt, 
                "cost": cost, 
                "reduce_description":reduce_description
            }

def process_request(description, jobid, location, ngrams=NGRAMS, overlap_limit=OVERLAPS_CONTEXT_THRESHOLD):

    cache = load_cache()
    #Cache hit
    if jobid in cache:
        print("[Cache HIT]", file=sys.stdout)
        response = cache[jobid]
        copy_response = response.copy()
        copy_response["source"] += copy_response["source"]+"-"+"[CACHED]"
        
        return copy_response
    
    # init values
    salary_min = salary_max = token_count_sent_chat_gpt = cost = 0.0 
    currency = all_context_join_with_location = time_lapse = " "
    source = "Not-sent-to-chat-gpt"
    salary_object = []

    _, contexts = get_context_from_numbers_in_text(text=description,
                                        ngrams=ngrams,
                                        overlap_limit=overlap_limit)
    
    if len(contexts)>0:
        location_normalized = remove_punctuation(normalize_text(location))

        if "argentina" in location_normalized:
            location_normalized=" "
        
        all_contexts_join = join_contexts(contexts=contexts)
        all_context_join_with_location = all_contexts_join+" "+location_normalized
        all_context_join_with_location = all_context_join_with_location.strip()

        try:
            with get_openai_callback() as cb:
                # older version
                # response = chain.predict_and_parse(text=(all_context_join_with_location))
                response = chain.predict(text=(all_context_join_with_location))
                source = "Chat-Gpt"

            token_count_sent_chat_gpt = cb.total_tokens
            cost = cb.total_cost

            if "data" in response:
                data = response["data"]
                if "salary" in data:
                    salary_object = data["salary"]
        except Exception as e:
            print("chain error: ", e, file=sys.stderr)
            print("-----------------------------------------------------", file=sys.stderr)
            print("Description: ", file=sys.stderr)
            print(all_contexts_join, file=sys.stderr)
            print("-----------------------------------------------------", file=sys.stderr)
    
        # not empty check
        if len(salary_object)==1:
            salary_range = salary_response = salary_object[0]

            try:
                
                #Backward comp
                if "range" in salary_response:
                    salary_range =  eval(salary_response["range"])

                if "single_value" in salary_range:
                    salary_min = salary_max = float(salary_range["single_value"])

                if "min" in salary_range:
                    salary_min = float(salary_range["min"])

                if "max" in salary_range:  
                    salary_max = float(salary_range["max"])
                #Backward comp

                if "salary_range_min" in salary_range:
                    salary_min = 0.0 if salary_range["salary_range_min"]=="" else float(salary_range["salary_range_min"])

                if "salary_range_max" in salary_range:  
                    salary_max = 0.0 if salary_range["salary_range_max"]=="" else float(salary_range["salary_range_max"])

                # this should not ever happen but just in case
                if salary_min==0.0 and salary_max>0.0:
                    salary_min = salary_max

                if salary_max==0.0 and salary_min>0.0:
                    salary_max = salary_min

                if "currency" in salary_response:
                    currency = salary_response["currency"]
                if "payment_period" in salary_response:
                    time_lapse = salary_response["payment_period"]

            except Exception as e:
                print("Not a dictionary: ", e)

    response = format_response(salary_min, salary_max, currency, time_lapse, source, token_count_sent_chat_gpt, cost, all_context_join_with_location)
    cache = save_cache(cache=cache, jobid=jobid, response=response)

    return response

app = Flask(__name__)
@app.route("/predict", methods=['POST'])
def predict():
    description = request.json['description']
    jobid = request.json['jobid']
    location = request.json.get('location')
    
    return process_request(description=description, jobid=jobid, location=location, ngrams=NGRAMS, overlap_limit=OVERLAPS_CONTEXT_THRESHOLD)
