import streamlit as st
import pandas as pd
from auth import authenticate_user, register_user, init_user_files
import re

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def login_page():
    """Main login page with user/admin selection"""
    st.set_page_config(page_title="EcoWatt Login", page_icon="⚡")

    # Initialize user files
    init_user_files()

    st.title("⚡ EcoWatt Login")

    # User type selection
    user_type = st.radio("Select User Type", ["User", "Admin"], horizontal=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        login_section(user_type.lower())

    with tab2:
        register_section(user_type.lower())

def login_section(user_type):
    """Login section"""
    st.subheader(f"{user_type.title()} Login")

    with st.form(f"{user_type}_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

        if submitted:
            if not username or not password:
                st.error("Please fill in all fields")
            else:
                user = authenticate_user(username, password, user_type)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.user_type = user_type
                    st.session_state.page = 'admin_dashboard' if user_type == 'admin' else 'user_dashboard'
                    st.success(f"Welcome back, {user['full_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

def register_section(user_type):
    """Registration section"""
    st.subheader(f"{user_type.title()} Registration")

    with st.form(f"{user_type}_register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        full_name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Register")

        if submitted:
            # Validation
            if not all([username, email, full_name, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address")
            elif len(username) < 3:
                st.error("Username must be at least 3 characters long")
            else:
                success, message = register_user(username, password, email, full_name, user_type)
                if success:
                    st.success(message)
                    st.info("You can now login with your credentials")
                else:
                    st.error(message)

if __name__ == "__main__":
    login_page()
