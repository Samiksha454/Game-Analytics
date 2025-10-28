import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import get_connection

st.set_page_config(page_title="Game Analytics Dashboard", layout="wide")

# -------------------------------------------
# 1. HEADER
# -------------------------------------------
st.title("🏆 Game Analytics Dashboard")
st.markdown("Analyze competitors, countries, and leaderboards in real time!")

# -------------------------------------------
# 2. DATABASE CONNECTION
# -------------------------------------------
conn = get_connection()
cursor = conn.cursor(dictionary=True)

# -------------------------------------------
# 3. HOMEPAGE DASHBOARD STATS
# -------------------------------------------
st.subheader("📊 Overview Statistics")

cursor.execute("SELECT COUNT(*) AS total_competitors FROM Competitors")
total_competitors = cursor.fetchone()['total_competitors']

cursor.execute("SELECT COUNT(DISTINCT country) AS total_countries FROM Competitors")
total_countries = cursor.fetchone()['total_countries']

cursor.execute("SELECT MAX(points) AS highest_points FROM Competitor_Rankings")
highest_points = cursor.fetchone()['highest_points']

col1, col2, col3 = st.columns(3)
col1.metric("Total Competitors", total_competitors)
col2.metric("Countries Represented", total_countries)
col3.metric("Highest Points Scored", highest_points)

st.divider()

# -------------------------------------------
# 4. COMPETITOR SEARCH & FILTER
# -------------------------------------------
st.subheader("🔍 Competitor Search & Filters")

name_search = st.text_input("Search by Competitor Name:")
rank_range = st.slider("Select Rank Range:", 1, 100, (1, 10))
country_filter = st.text_input("Filter by Country:")
points_threshold = st.number_input("Minimum Points:", min_value=0, value=0)

query = """
    SELECT c.name, c.country, cr.rank_position, cr.points, cr.movement
    FROM Competitors c
    JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
    WHERE cr.rank_position BETWEEN %s AND %s
"""
params = [rank_range[0], rank_range[1]]

if name_search:
    query += " AND c.name LIKE %s"
    params.append(f"%{name_search}%")
if country_filter:
    query += " AND c.country LIKE %s"
    params.append(f"%{country_filter}%")
if points_threshold > 0:
    query += " AND cr.points >= %s"
    params.append(points_threshold)

cursor.execute(query, tuple(params))
competitor_data = cursor.fetchall()
df_competitors = pd.DataFrame(competitor_data)

st.dataframe(df_competitors)

st.divider()

# -------------------------------------------
# 5. COMPETITOR DETAILS VIEWER
# -------------------------------------------
st.subheader("📋 Competitor Details")

selected_competitor = st.selectbox(
    "Select a Competitor", 
    options=df_competitors['name'].unique() if not df_competitors.empty else []
)

if selected_competitor:
    cursor.execute("""
        SELECT c.name, c.country, cr.rank_position, cr.points, cr.movement
        FROM Competitors c
        JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
        WHERE c.name = %s
    """, (selected_competitor,))
    details = cursor.fetchone()

    st.write("**Country:**", details['country'])
    st.write("**Rank:**", details['rank_position'])
    st.write("**Points:**", details['points'])
    st.write("**Movement:**", details['movement'])

st.divider()

# -------------------------------------------
# 6. COUNTRY-WISE ANALYSIS
# -------------------------------------------
st.subheader("🌍 Country-Wise Analysis")

cursor.execute("""
    SELECT c.country, COUNT(c.competitor_id) AS total_competitors, 
           AVG(cr.points) AS avg_points
    FROM Competitors c
    JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
    GROUP BY c.country
    ORDER BY avg_points DESC
""")
country_data = cursor.fetchall()
df_country = pd.DataFrame(country_data)

st.dataframe(df_country)

fig = px.bar(df_country, x="country", y="avg_points", 
             color="total_competitors", 
             title="Average Points by Country")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------
# 7. LEADERBOARDS
# -------------------------------------------
st.subheader("🏅 Leaderboards")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Top Ranked Competitors")
    cursor.execute("""
        SELECT c.name, c.country, cr.rank_position, cr.points
        FROM Competitors c
        JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
        ORDER BY cr.rank_position ASC
        LIMIT 10
    """)
    top_ranked = cursor.fetchall()
    st.dataframe(pd.DataFrame(top_ranked))

with col2:
    st.markdown("#### Highest Points Competitors")
    cursor.execute("""
        SELECT c.name, c.country, cr.points, cr.rank_position
        FROM Competitors c
        JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
        ORDER BY cr.points DESC
        LIMIT 10
    """)
    top_points = cursor.fetchall()
    st.dataframe(pd.DataFrame(top_points))

cursor.close()
conn.close()
