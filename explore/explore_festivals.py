import streamlit as st
import pandas as pd
from db.database import get_connection
import pydeck as pdk
import os

CATEGORY_MAP = {
    "Religious": "🕉️ Religious",
    "Cultural": "🎭 Cultural",
    "Regional": "📍 Regional",
    "National": "🇮🇳 National"
}

def load_festival_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM festivals", conn)
    conn.close()
    return df

def explore_festivals():
    st.subheader("🔍 Explore Indian Festivals")

    df = load_festival_data()

    if df.empty:
        st.warning("No festival data available.")
        return

    df['upload_time'] = pd.to_datetime(df['upload_time'])

    with st.sidebar:
        st.markdown("### 🗂️ Filters")

        selected_category = st.multiselect(
            "Select Category", options=df["category"].unique(), default=df["category"].unique()
        )

        selected_month = st.selectbox("Select Month", ["All"] + list(range(1, 13)))

    # Apply filters
    filtered_df = df[df["category"].isin(selected_category)]

    if selected_month != "All":
        filtered_df = filtered_df[filtered_df["upload_time"].dt.month == int(selected_month)]

    st.write(f"📄 Showing {len(filtered_df)} result(s).")

    # Map
    st.map(filtered_df[["latitude", "longitude"]], zoom=4)

    # Festival cards
    for _, row in filtered_df.iterrows():
        with st.expander(f"📌 {row['title']}"):
            st.markdown(f"**Description:** {row['description'][:300]}...")
            st.markdown(f"**Category:** {CATEGORY_MAP.get(row['category'], row['category'])}")
            st.markdown(f"**Location:** ({row['latitude']}, {row['longitude']})")
            st.markdown(f"**Uploaded on:** {row['upload_time'].date()}")
            if row["filetype"] in ["jpg", "png"]:
                st.image(row["filename"], use_column_width=True)
            elif row["filetype"] in ["mp3", "wav"]:
                st.audio(row["filename"])
            elif row["filetype"] in ["mp4", "mov"]:
                st.video(row["filename"])
            elif row["filetype"] == "txt":
                with open(row["filename"], "r", encoding="utf-8") as f:
                    st.text(f.read()[:500])
