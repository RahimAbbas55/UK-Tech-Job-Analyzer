<div align="center">

# 🇬🇧 UK Data Science / AI Job Market Analyser

**An interactive dashboard analysing live UK data science and AI job listings —
salary trends, in-demand skills, seniority mix, and hiring patterns.**

Built using the official Reed.co.uk Jobseeker API.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Automated](https://img.shields.io/badge/Data%20Refresh-Automated%20every%203%20days-2ea44f)](#-automated-data-refresh)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://uk-tech-job-analyzer-ks.streamlit.app/)

**[→ View the live dashboard](https://uk-tech-job-analyzer-ks.streamlit.app/)**

</div>

---

## 📋 Contents

- [System Architecture](#-system-architecture)
- [What It Does](#-what-it-does)
- [Data Quality Notes](#-data-quality-notes)
- [Automated Data Refresh](#-automated-data-refresh)
- [Stack](#-stack)
- [Setup](#-setup)
- [Screenshots](#-screenshots)
- [Author](#-author)

---

## 🏗️ System Architecture

```mermaid
graph LR
    A[Reed.co.uk API] -->|fetch_reed.py| B[raw_jobs.csv]
    B -->|clean_data.py| C[clean_jobs.csv]
    C -->|app.py| D[Streamlit Dashboard]

    A2[Reed API: job details] -->|full descriptions| B

    style A fill:#2d5986,color:#fff
    style A2 fill:#2d5986,color:#fff
    style D fill:#4a8b3a,color:#fff
```

**Pipeline stages:**

| Stage | Script | Purpose |
|---|---|---|
| 1️⃣ Collect | `fetch_reed.py` | Searches Reed's API for data/AI roles, then fetches full job descriptions per listing (search results alone are truncated) |
| 2️⃣ Clean | `clean_data.py` | Parses salaries, extracts skills via regex, detects seniority, filters agencies |
| 3️⃣ Present | `app.py` | Streamlit dashboard with interactive Plotly charts |

---

## ✨ What It Does

- 🔍 Pulls live job listings across data scientist, data analyst, and ML engineer roles
- 📄 Fetches full job descriptions (not just search snippets) for accurate skill detection
- 🧹 Extracts skills, seniority level, and salary data using regex-based parsing
- 🏢 Filters out recruitment agencies and training providers to surface genuine hiring employers
- 📊 Visualises everything in an interactive Streamlit dashboard

---

## 🔎 Data Quality Notes

Real issues found and fixed while building this — not just tutorial-following:

- **Truncated descriptions:** Reed's search endpoint caps job descriptions at ~450
  characters. Switched to per-job detail calls to pull full text, which meaningfully
  improved skill-detection accuracy.
- **Misleading "top employers":** Some of the top posters were actually training
  providers or recruitment agencies, not genuine hiring companies. Added keyword +
  manual filtering to surface real employers.

---

## 🔄 Automated Data Refresh

Job data refreshes automatically every 3 days via a scheduled **GitHub Actions**
workflow — no manual re-running required. It fetches fresh listings, rebuilds the
cleaned dataset, and commits the update back to the repo automatically.

<table>
<tr>
<td align="center"><b>Workflow running</b><br><img src="screenshots/github_action_running.png" width="280"></td>
<td align="center"><b>Successful run</b><br><img src="screenshots/github_action_1.png" width="280"></td>
<td align="center"><b>Confirmed complete</b><br><img src="screenshots/github_action_2.png" width="280"></td>
</tr>
</table>

---

## 🛠️ Stack

`Python` · `Pandas` · `Plotly` · `Streamlit` · `Reed.co.uk API` · `GitHub Actions`

---

## ⚙️ Setup

```bash
# 1. Get a free API key
# https://www.reed.co.uk/developers/jobseeker

# 2. Create and activate a virtual environment
python3 -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
echo "REED_API_KEY=your_key_here" > .env

# 5. Run the pipeline
python src/fetch_reed.py
python src/clean_data.py

# 6. Launch the dashboard
streamlit run app.py
```

---

## 📸 Screenshots

**Salary distribution by role**
![Salary box plot](screenshots/box_plot.png)

**Most in-demand skills**
![In-demand skills](screenshots/demand_skills.png)

**Seniority mix & top hiring companies**
![Seniority and companies](screenshots/Seniority_Companies.png)

---

## 👤 Author

**Rahim Abbas**
Built while researching my own transition into data science/AI roles in the UK.

[![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/RahimAbbas55)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rahim-abbas-b5520b258/)