import streamlit as st
from auth.login import login
from auth.register import register
from db.database import create_tables

# Set up Streamlit page
st.set_page_config(page_title="Bharatiy Utsav", layout="centered")
st.title("🎉 Bharatiy Utsav")

# Initialize database tables
create_tables()

# Initialize user session
if "user" not in st.session_state:
    st.session_state["user"] = None

# Navigation menu
if st.session_state["user"]:
    menu = ["Upload Festival", "Explore Festivals", "AI Assistant", "Logout"]
else:
    menu = ["Login", "Register"]

choice = st.sidebar.selectbox("Navigate", menu)

# Route based on selection
if choice == "Login":
    login()

elif choice == "Register":
    register()

elif choice == "Upload Festival":
    from upload.upload_handler import upload_festival
    upload_festival()

elif choice == "Explore Festivals":
    from explore.explore_festivals import explore_festivals
    explore_festivals()

elif choice == "AI Assistant":
    from ai.ai_assistant import ai_festival_assistant
    ai_festival_assistant()

elif choice == "Logout":
    st.session_state["user"] = None
    st.success("Logged out successfully.")
    st.rerun()
