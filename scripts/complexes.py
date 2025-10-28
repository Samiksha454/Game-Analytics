# scripts/complexes.py
from sportradar_client import get_json
import pandas as pd, json, os

ENDPOINT = "complexes.json"  

raw_path = os.path.join("raw_json", "complexes.json")
data = get_json(ENDPOINT, save_path=raw_path)


complexes = data.get("complexes", [])
comp_rows, venue_rows = [], []
for c in complexes:
    comp_rows.append({
        "complex_id": c.get("id"),
        "complex_name": c.get("name"),
        "num_venues": len(c.get("venues", [])),
        "raw_json": json.dumps(c)
    })
    for v in c.get("venues", []):
        venue_rows.append({
            "venue_id": v.get("id"),
            "complex_id": c.get("id"),
            "venue_name": v.get("name"),
            "city_name": v.get("city_name"),
            "country_name": v.get("country_name"),
            "country_code": v.get("country_code"),
            "timezone": v.get("timezone"),
            "raw_json": json.dumps(v)
        })

os.makedirs("csv", exist_ok=True)
pd.DataFrame(comp_rows).to_csv("csv/complexes.csv", index=False)
pd.DataFrame(venue_rows).to_csv("csv/venues.csv", index=False)
print("Saved csv/complexes.csv and csv/venues.csv")
