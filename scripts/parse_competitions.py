import json
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="sports_user",          # your DB user
    password="Horse1@@",         # your password
    database="sportradar_db"
)
cursor = conn.cursor()

# Load competitions.json
with open("raw_json/competitions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

competitions = data["competitions"]

for comp in competitions:
    cat = comp["category"]

     #Safely extract parent_id (if exists)
    parent = comp.get("parent")
    parent_id = parent["id"] if parent else None

    # Insert category
    cursor.execute("""
        INSERT IGNORE INTO Categories (category_id, category_name)
        VALUES (%s, %s)
    """, (cat["id"], cat["name"]))

    # Insert competition
    cursor.execute("""
        INSERT IGNORE INTO Competitions 
        (competition_id, competition_name, category_id, type, gender, parent_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (comp["id"], comp["name"], cat["id"], comp.get("type"), comp.get("gender"), parent_id))


conn.commit()
cursor.close()
conn.close()

print("Competitions and Categories data inserted successfully.")
