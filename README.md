# Game Analytics Project

## Overview
The **Game Analytics Dashboard** is an interactive data-driven web application built using **Streamlit** and **MySQL**.  
It analyzes global sports data, including competitions, venues, and competitor performance.

---

## Objectives
- Extract, clean, and load JSON sports data into MySQL.
- Perform SQL-based analytics on competitions, venues, and rankings.
- Develop an interactive **Streamlit Dashboard** for visual insights.
- Enable dynamic filtering, leaderboards, and country-wise analysis.

---

## Tech Stack
- **Python** (pandas, mysql-connector, streamlit)
- **MySQL** for data storage
- **JSON** for data ingestion

---

## Project Structure
Game_Analytics/
│
├── raw_json/
│ └── competitions.json
│
├── scripts/
│ ├── parse_competitions.py
│ ├── parse_venues.py
│ ├── parse_rankings.py
│
├── sql/
│ ├── database_schema.sql
│ ├── sql_queries_documentation.sql
│
├── streamlit_app/
│ ├── app.py
│ └── db_config.py
│
└── README.md
