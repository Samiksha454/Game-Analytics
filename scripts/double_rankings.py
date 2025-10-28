# scripts/doubles_rankings.py
from sportradar_client import get_json
import pandas as pd, json, os

# Endpoint for doubles competitor rankings
ENDPOINT = "double_competitors_rankings.json"  

raw_path = os.path.join("raw_json", "double_competitors_rankings.json")
data = get_json(ENDPOINT, save_path=raw_path)

# Extract rankings list
rankings = data.get("rankings", [])

ranking_rows, competitor_rows = [], []

for r in rankings:
    # Basic ranking metadata
    ranking_info = {
        "type_id": r.get("type_id"),
        "ranking_name": r.get("name"),
        "year": r.get("year"),
        "week": r.get("week"),
        "gender": r.get("gender")
    }

    for c in r.get("competitor_rankings", []):
        competitor = c.get("competitor", {})
        
        #Competitor info
        competitor_rows.append({
            "competitor_id": competitor.get("id"),
            "name": competitor.get("name"),
            "country": competitor.get("country"),
            "country_code": competitor.get("country_code"),
            "abbreviation": competitor.get("abbreviation"),
            "raw_json": json.dumps(competitor)
        })
        
        #Ranking info for each competitor
        ranking_rows.append({
            "competitor_id": competitor.get("id"),
            "ranking_name": r.get("name"),
            "gender": r.get("gender"),
            "year": r.get("year"),
            "week": r.get("week"),
            "rank": c.get("rank"),
            "movement": c.get("movement"),
            "points": c.get("points"),
            "competitions_played": c.get("competitions_played"),
            "raw_json": json.dumps(c)
        })

#Save to CSV files
os.makedirs("csv", exist_ok=True)
pd.DataFrame(ranking_rows).to_csv("csv/competitor_rankings.csv", index=False)
pd.DataFrame(competitor_rows).drop_duplicates(subset=["competitor_id"]).to_csv("csv/competitors.csv", index=False)

print("Saved csv/competitor_rankings.csv and csv/competitors.csv")
# print(pd.DataFrame(ranking_rows).head())
