import streamlit as st
import os
import uuid
from datetime import datetime
from db.database import get_connection
from ai.whisper_transcribe import transcribe_audio
from ai.summarizer import summarize_text

UPLOAD_DIR = "assets/uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

CATEGORIES = ["Religious", "Cultural", "Regional", "National"]

def save_file(uploaded_file):
    file_id = str(uuid.uuid4())
    extension = uploaded_file.name.split(".")[-1]
    filename = f"{file_id}.{extension}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())
    return filepath, extension

def insert_festival_data(user_id, title, desc, category, lat, lon, filename, filetype):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO festivals (user_id, title, description, category, latitude, longitude, filename, filetype)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, title, desc, category, lat, lon, filename, filetype))
    conn.commit()
    conn.close()

def upload_festival():
    st.subheader("📤 Upload Festival Information")

    if not st.session_state.get("user"):
        st.warning("Please log in to upload data.")
        return

    title = st.text_input("Festival Title")
    description = st.text_area("Festival Description")
    category = st.selectbox("Category", CATEGORIES)
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    uploaded_file = st.file_uploader("Upload File (audio/video/image/text)", type=["mp3", "wav", "mp4", "mov", "jpg", "png", "txt"])

    if st.button("Submit"):
        if not (title and description and uploaded_file):
            st.error("Please fill all fields and upload a file.")
            return

        st.info("Saving file...")
        filepath, ext = save_file(uploaded_file)

        summary = ""
        if ext in ["mp3", "wav", "mp4", "mov"]:
            st.info("Transcribing with Whisper...")
            transcription = transcribe_audio(filepath)
            summary = summarize_text(transcription)
            st.text_area("📝 Transcription", transcription, height=150)
            st.text_area("🧠 Summary", summary, height=100)
            description += f"\n\nAuto Summary: {summary}"

        elif ext == "txt":
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()
            summary = summarize_text(raw_text)
            st.text_area("🧠 Summary", summary, height=100)
            description += f"\n\nAuto Summary: {summary}"

        insert_festival_data(
            user_id=st.session_state["user"]["id"],
            title=title,
            desc=description,
            category=category,
            lat=lat,
            lon=lon,
            filename=filepath,
            filetype=ext
        )

        st.success("✅ Festival data uploaded successfully!")
