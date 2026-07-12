# File where data cleaning and enrichment happens
import re
import os
import pandas as pd

# Define patterns for skills
SKILL_KEYWORDS = {
    "Python": [r"\bpython\b"],
    "SQL": [r"\bsql\b"],
    "Machine Learning": [r"machine learning", r"\bml\b"],
    "AWS": [r"\baws\b"],
    "Tableau": [r"\btableau\b"],
    "Power BI": [r"power ?bi"],
}

# Define patterns for seniority levels
SENIORITY_PATTERNS = {
    "Intern/Graduate": [r"intern", r"graduate", r"junior", r"entry.level"],
    "Senior": [r"senior", r"lead", r"principal", r"staff"],
    "Manager/Director": [r"manager", r"director", r"head of"],
}

# Fetch particular skills from the string of text
def detect_skills(text):
    text = text.lower()
    found = []
    for skill , patterns in SKILL_KEYWORDS.items():
        for pattern in patterns:
            if re.search(pattern , text):
                found.append(skill)
                break
    return found

# Function to parse salary range from a row of data
def parse_salary(row):
    lo = row.get("minimumSalary")
    hi = row.get("maximumSalary")
    # Handle cases where the salary is not a number
    try:
        lo = float(lo)
    except (TypeError , ValueError):
        lo = None
    # Handle cases where the salary is not a number
    try: 
        hi = float(hi)
    except (TypeError , ValueError):
        hi = None
    return lo , hi

# Function to detect seniority level from a title
def detect_seniority(title):
    title = title.lower()
    for level , patterns in SENIORITY_PATTERNS.items():
        for p in patterns:
            if re.search(p , title):
                return level
    return "Mid-level"  # Default if no match found

# Function to clean and enrich the data
def clean(df):
    df = df.copy()
    # Enrich the salary data 
    salaries = df.apply(parse_salary , axis = 1 , result_type = "expand")
    df["salary_min"] = salaries[0]
    df["salary_max"] = salaries[1]
    df["salary_mid"] = df[["salary_min" , "salary_max"]].mean(axis = 1)
    
    # Enrich the skills data
    df["skills"] = df.get("jobDescription" , "")
    df["jobDescription"] = df["jobDescription"].fillna("")
    df["jobTitle"] = df["jobTitle"].fillna("")
    df["scan_text"] = df["jobTitle"] + " " + df["jobDescription"]
    df["skills"] = df["scan_text"].apply(detect_skills)
    
    # Enrich the seniority data
    df["seniority"] = df["jobTitle"].apply(detect_seniority)
    
    if "locationName" in df.columns:
        df["locationName"] = df["locationName"].fillna("Unknown").str.strip()
    df = df.drop(columns = ["scan_text"])
    df = df[ df["jobTitle"] != "" ]
    return df

# Main function to read, clean, and save the data
def main():
    if not os.path.exists("data/raw_jobs.csv"):
        print("Raw data file not found. Please run: src/fetch_reed.py first.")
        return
    raw = pd.read_csv("data/raw_jobs.csv")
    cleaned = clean(raw)
    cleaned.to_csv("data/clean_jobs.csv", index=False)
    print(f"Cleaned {len(cleaned)} jobs -> data/clean_jobs.csv")

if __name__ == "__main__":
    main()