from serpapi import GoogleSearch
import requests

def job_search(q, api_key,
               location = None, uule = None,
               google_domain = "google.com", gl = None, hl = None,
               start = 0,
               chips = None, lrad = None, ltype = None,
               engine = "google_jobs", no_cache = False, async_ = False, output = "json"):
    
    params = {"q"             : q,
              "api_key"       : api_key,
              "location"      : location,
              "uule"          : uule,
              "google_domain" : google_domain,
              "gl"            : gl,
              "hl"            : hl,
              "start"         : start,
              "chips"         : chips,
              "lrad"          : lrad,
              "ltype"         : ltype,
              "engine"        : engine,
              "no_cache"      : no_cache,
              "async"         : async_,
              "output"        : output}
    
    search = GoogleSearch(params)

    return search.get_dict()
    
    """
    - Search Query:
    q: required (string): Parameter defines the query you want to search.
    
    - Geographic Location:
    location: optional (string): 
    \tParameter defines from where you want the search to originate.
    \tIf several locations match the location requested, we'll pick the most popular one.
    \tHead to the https://serpapi.com/locations-api API if you need more precise control.
    \tlocation and uule parameters can't be used together.
    \tAvoid utilizing location when setting the location outside the U.S. when using Google Shopping and/or Google Product API.
    
    uule: optional ():
    \tParameter is the Google encoded location you want to use for the search.
    \tuule and location parameters can't be used together.
    
    - Localization:
    google_domain: optional (string): default: 'google.com'
    \tParameter defines the Google domain to use. It defaults to google.com.
    \tHead to the [Google domains page](https://serpapi.com/google-domains) for a full list of supported Google domains.
    
    gl: optional: (string):
    \tParameter defines the country to use for the Google search.
    \tIt's a two-letter country code. (e.g., us for the United States, uk for United Kingdom, or fr for France)
    \tHead to the [Google countries page](https://serpapi.com/google-countries) for a full list of supported Google countries.
    
    hl: optional: (string): default: en
    \tParameter defines the language to use for the Google Jobs search.
    \tIt's a two-letter language code. (e.g., en for English, es for Spanish, or fr for French).
    \tHead to the [Google languages page](https://serpapi.com/google-languages) for a full list of supported Google languages.
    
    - Pagination:
    start: optional: (integer): default: 0
    \tParameter defines the result offset. It skips the given number of results.
    \tIt's used for pagination. (e.g., 0 (default) is the first page of results, 10 is the 2nd page of results, 20 is the 3rd page of results, etc.).
    
    - Advanced Google Jobs Parameter:
    chips: optional: (string):
    \tParameter defines additional query conditions.
    \tTop of a job search page contains elements called chips, its values are extracted in order to be passed to chips parameter.
    \tE.g. city:Owg_06VPwoli_nfhBo8LyA== will return results for New York.
    
    lrad: optional: (integer): default: None
    \tDefines search radius in kilometers. Does not strictly limit the radius.
    
    ltype: optional: (boolean): False
    \tParameter will filter the results by work from home.
    
    - SerpApi Parameters:
    engine: required (string): default: 'google_jobs'
    \tSet parameter to google_jobs to use the Google Jobs API engine.
    
    no_chace: optional: (boolean): default: False
    \tParameter will force SerpApi to fetch the Google Jobs results even if a cached version is already present.
    \tA cache is served only if the query and all parameters are exactly the same.
    \tCache expires after 1h. Cached searches are free, and are not counted towards your searches per month.
    \tIt can be set to false (default) to allow results from the cache, or true to disallow results from the cache.
    \tno_cache and async parameters should not be used together.
    
    async: optional: (boolean): default: False
    \tParameter defines the way you want to submit your search to SerpApi.
    \tIt can be set to false (default) to open an HTTP connection and keep it open until you got your search results, or true to just submit your search to SerpApi and retrieve them later.
    \tIn this case, you'll need to use our (Searches Archive API)[https://serpapi.com/search-archive-api] to retrieve your results.
    \tasync and no_cache parameters should not be used together.
    \tasync should not be used on accounts with [Ludicrous Speed](https://serpapi.com/plan) enabled.
    
    api_key: required: (string):
    \tParameter defines the SerpApi private key to use.
    
    output: optional: (string): default: 'json'
    \tParameter defines the final output you want.
    \tIt can be set to 'json' (default) to get a structured JSON of the results, or 'html' to get the raw html retrieved.
    
    
    API Results:
    JSON:
    \tJSON output includes structured data for jobs_results - actual search results and chips - data extracted from the top of the job search page and can be used detailed query.
    \tA search status is accessible through search_metadata.status. It flows this way: Processing -> Success || Error. If a search has failed, error will contain an error message. search_metadata.id is the search ID inside SerpApi.
    
    HTML:
    \tHTML output is useful to debug JSON results or support features not supported yet by SerpApi.
    \tHTML output gives you the raw HTML results from Google.
    
    Endpoint with requests:
    
    https://serpapi.com/search.json?engine=google_jobs&q=barista+new+york&hl=en
    
    
    """

def search_archive(q_id, api_key):

    endpoint = f"https://serpapi.com/searches/{q_id}.json?api_key={api_key}"

    response = requests.get(url = endpoint)

    return response.json() 


