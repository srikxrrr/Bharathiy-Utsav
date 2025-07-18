import streamlit as st
from auth.auth_utils import register_user

def register():
    st.subheader("📝 Register")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm:
            st.error("Passwords do not match!")
        elif register_user(name, email, password):
            st.success("Registered successfully. Please login.")
        else:
            st.error("User with this email already exists.")
