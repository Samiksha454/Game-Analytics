# scripts/competitions.py
from sportradar_client import get_json
import pandas as pd, os

ENDPOINT = "competitions.json"  

raw_path = os.path.join("raw_json", "competitions.json")
data = get_json(ENDPOINT, save_path=raw_path)

# adapt parsing to actual JSON structure returned
items = data.get("competitions", [])
rows = []
for c in items:
    category = c.get("category", {})
    rows.append({
        "competition_id": c.get("id"),
        "competition_name": c.get("name"),
        "type": c.get("type"),
        "gender": c.get("gender"),
        "category_id": category.get("id"),
        "category_name": category.get("name"),
    })

df = pd.json_normalize(rows)
os.makedirs("csv", exist_ok=True)
df.to_csv("csv/competitions.csv", index=False)
print("Saved csv/competitions.csv")
