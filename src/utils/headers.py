import os
from dotenv import load_dotenv
load_dotenv()
APITOKEN = os.getenv("TMDBTOKEN")

def headersTmdb():
    headers = {
        "Authorization": f"{APITOKEN}",
        "Accept": "application/json"
    }
    return headers

def headersScraping():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    return headers