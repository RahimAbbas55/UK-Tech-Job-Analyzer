# Streamlit dashboard app
import ast
import pandas as pd
import streamlit as st
import plotly.express as px
from collections import Counter

TRAINING_PROVIDERS = [
    "Newto Training", "ITOL Recruit", "IT Career Switch"
]
AGENCY_KEYWORDS = [
    "recruit", "staffing", "talent", "training", "career switch", "consulting"
]
NAMED_AGENCIES = [
    "Robert Walters", "Oscar Technology", "Harnham - Data & Analytics Recruitment"
]

def is_likely_agency(name):
    name_lower = str(name).lower()
    if any(keyword in name_lower for keyword in AGENCY_KEYWORDS):
        return True
    if name in NAMED_AGENCIES:
        return True
    return False

st.set_page_config(page_title = "UK Data/AI Job Market" , layout = "wide")
@st.cache_data
def load_data():
    df = pd.read_csv("data/clean_jobs.csv")
    df["skills"] =df["skills"].apply(ast.literal_eval)
    return df
df = load_data()
st.title("UK Data/AI Job Market Dashboard")
st.caption(f"Based on {len(df):,} live job listings from Reed.co.uk")
col1 , col2 , col3 = st.columns(3)
col1.metric("Total Jobs" , f"{len(df):,}")
col2.metric("With salary disclosed", f"{df['salary_mid'].notna().sum():,}")
if df["salary_mid"].notna().any():
    col3.metric("Median salary", f"£{df['salary_mid'].median():,.0f}")
else:
    col3.metric("Median salary", "N/A")

# Box Plot
st.divider()
st.subheader("💰 Salary Distribution by Role")
salary_df = df.dropna(subset = ["salary_mid"])
if not salary_df.empty:
    fig = px.box(
        salary_df,
        x="search_term",
        y="salary_mid",
        color="search_term",
        points="all",
        labels={"search_term": "Role", "salary_mid": "Salary (£/year)"},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width = "stretch")
else:
    st.info("No salary data available.")

# Skills Bar Chart
st.divider()
st.subheader("🛠️ Most in Demand Skills")
all_skills = []
for skill_list in df["skills"]:
    all_skills.extend(skill_list)
skill_counts = Counter(all_skills)
if skill_counts:
    skills_df = pd.DataFrame(skill_counts.items() , columns=["Skills" , "Mentions"])
    skills_df = skills_df.sort_values("Mentions" , ascending = True)
    fig2 = px.bar(skills_df , x = "Mentions" , y = "Skills" , orientation = "h")
    st.plotly_chart(fig2 , width = "stretch")
else:
    st.info("No skills data available!")   

# Seniority & Hiring Companies Graph
st.divider()
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📊 Seniority Mix")
    seniority_counts = df["seniority"].value_counts()
    fig3 = px.pie(values=seniority_counts.values, names=seniority_counts.index)
    st.plotly_chart(fig3, width = "stretch")

with col_b:
    st.subheader("🏢 Top Hiring Companies")
    real_employers = df[~df["employerName"].apply(is_likely_agency)]
    top_companies = real_employers["employerName"].value_counts().head(10).reset_index()
    top_companies.columns = ["Company", "Open Roles"]
    top_companies = top_companies.sort_values("Open Roles")
    fig4 = px.bar(top_companies, x="Open Roles", y="Company", orientation="h")
    st.plotly_chart(fig4, width='stretch')