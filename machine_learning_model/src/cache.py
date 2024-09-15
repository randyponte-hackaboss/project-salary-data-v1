import os
import pickle

CACHE_PATH = os.environ["CACHE_PATH"] if "CACHE_PATH" in os.environ else "cache.pkl"

def load_cache():
    cache = dict()

    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as file:
            cache = pickle.loads(file.read())
    
    return cache

def save_cache(cache, jobid, response):
    # Save if processed by chatgpt
    if response["source"] == "Chat-Gpt":
        copy_response = response.copy()
        cache[jobid] = copy_response

        with open(CACHE_PATH, "wb") as file:
            file.write(pickle.dumps(cache))

    return cache
