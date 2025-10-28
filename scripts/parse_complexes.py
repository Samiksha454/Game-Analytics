import json
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="sports_user",
    password="Horse1@@",
    database="sportradar_db"
)
cursor = conn.cursor()

# Load complexes.json
with open("raw_json/complexes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

complexes = data["complexes"]

for c in complexes:
    cursor.execute("""
        INSERT IGNORE INTO Complexes (complex_id, complex_name)
        VALUES (%s, %s)
    """, (c["id"], c["name"]))

    for v in c.get("venues", []):
        cursor.execute("""
            INSERT IGNORE INTO Venues (venue_id, venue_name, city_name, country_name, timezone, complex_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (v["id"], v["name"], v.get("city_name"), v.get("country_name"), v.get("timezone"), c["id"]))

conn.commit()
cursor.close()
conn.close()

print("Complexes and Venues data inserted successfully.")
