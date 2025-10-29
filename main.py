import streamlit as st

# Main application entry point
def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.page = 'login'

    # Route to appropriate page
    if not st.session_state.logged_in or st.session_state.page == 'login':
        from login import login_page
        login_page()
    elif st.session_state.page == 'user_dashboard':
        # Import and run user dashboard
        from app import user_dashboard
        user_dashboard()
    elif st.session_state.page == 'admin_dashboard':
        from admin_dashboard import admin_dashboard
        admin_dashboard()

if __name__ == "__main__":
    main()
