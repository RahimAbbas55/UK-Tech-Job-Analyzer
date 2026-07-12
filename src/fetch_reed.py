# Fetch the data from Reed API
import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override = True)  # Load environment variables from .env file

REED_API_URL = "https://www.reed.co.uk/api/1.0/search"
SEARCH_TERMS = [
    "data scientists",
    "data analyst",
    "machine learning engineer"
]

def fetch_jobs_for_term(term , api_key , max_results = 100):
    all_results = []
    skip = 0
    while skip < max_results:
        params = {
            "keywords" : term,
            "locationName" : "UK",
            "resultsToTake" : 100,
            "resultsToSkip" : skip
        }
        response = requests.get(REED_API_URL, params = params , auth = (api_key , ''))
        if response.status_code != 200:
            print(f"Something went wrong! Status code : {response.status_code}")
            break
        data = response.json()
        jobs = data.get("results" , [])
        
        if not jobs:
            break
        all_results.extend(jobs)
        skip += 100
        time.sleep(0.5)
    print(f"{term} : found {len(all_results)} jobs!")
    return all_results

# Main caller function
def main():
    api_key = os.environ.get("REED_API_KEY")
    if not api_key:
        print(f"No Api key found! Run: export REED_API_KEY='your_key_here'")
        return
    all_jobs = []
    for term in SEARCH_TERMS:
        jobs = fetch_jobs_for_term(term , api_key)
        for job in jobs:
            job["search_term"] = term
        all_jobs.extend(jobs)
    df = pd.DataFrame(all_jobs)
    df = df.drop_duplicates(subset = ["jobId"])
    os.makedirs("data" , exist_ok = True)
    df.to_csv("data/raw_jobs.csv" , index = False)
    print(f"Saved {len(df)} unique jobs to data/raw_jobs.csv")
    
if __name__ == "__main__":
    main()