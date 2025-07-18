import streamlit as st
from auth.auth_utils import login_user

def login():
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state["user"] = user
            st.success(f"Welcome back, {user['name']}!")
            st.rerun()
        else:
            st.error("Invalid credentials")
