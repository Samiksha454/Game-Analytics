import json
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="sports_user",
    password="Horse1@@",
    database="sportradar_db"
)
cursor = conn.cursor()

# Load rankings file
with open("raw_json/double_competitors_rankings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for ranking in data["rankings"]:
    for r in ranking["competitor_rankings"]:
        comp = r["competitor"]

        # Insert competitor
        cursor.execute("""
            INSERT IGNORE INTO Competitors (competitor_id, name, country, country_code)
            VALUES (%s, %s, %s, %s)
        """, (comp["id"], comp["name"], comp.get("country"), comp.get("country_code")))

        # Insert ranking
        cursor.execute("""
            INSERT INTO Competitor_Rankings (competitor_id, rank_position, movement, points)
            VALUES (%s, %s, %s, %s)
        """, (comp["id"], r["rank"], r.get("movement", 0), r.get("points", 0)))

conn.commit()
cursor.close()
conn.close()

print("Competitors and Rankings data inserted successfully.")
