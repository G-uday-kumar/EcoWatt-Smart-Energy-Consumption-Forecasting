import streamlit as st
import pandas as pd
from auth import get_all_users, get_all_admin_users, delete_user
from data_generator import generate_energy_data
from model import prepare_data, train_model, predict_future, load_model, save_model
import matplotlib.pyplot as plt
import os

def admin_dashboard():
    """Admin dashboard with user management and system overview"""
    st.set_page_config(page_title="EcoWatt Admin Dashboard", page_icon="⚡")

    if not st.session_state.get('logged_in') or st.session_state.get('user_type') != 'admin':
        st.error("Access denied. Admin login required.")
        return

    st.title("⚡ EcoWatt Admin Dashboard")
    st.markdown(f"Welcome, {st.session_state.user['full_name']}!")

    # Sidebar navigation
    page = st.sidebar.selectbox("Navigation", [
        "Dashboard Overview",
        "User Management",
        "System Data",
        "Analytics"
    ])

    if page == "Dashboard Overview":
        dashboard_overview()
    elif page == "User Management":
        user_management()
    elif page == "System Data":
        system_data_management()
    elif page == "Analytics":
        analytics_section()

    # Logout button
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def dashboard_overview():
    """Main dashboard overview"""
    st.header("Dashboard Overview")

    # System statistics
    col1, col2, col3, col4 = st.columns(4)

    users_df = get_all_users()
    admin_df = get_all_admin_users()

    with col1:
        st.metric("Total Users", len(users_df))
    with col2:
        st.metric("Total Admins", len(admin_df))
    with col3:
        st.metric("System Status", "Active")
    with col4:
        data_exists = os.path.exists('energy_data.csv')
        st.metric("Data Available", "Yes" if data_exists else "No")

    # Recent activity
    st.subheader("Recent Activity")
    st.info("System initialized and running normally")
    st.info(f"Last login: {st.session_state.user.get('username', 'Unknown')}")

def user_management():
    """User management section"""
    st.header("User Management")

    tab1, tab2 = st.tabs(["Regular Users", "Admin Users"])

    with tab1:
        manage_users("user")
    with tab2:
        manage_users("admin")

def manage_users(user_type):
    """Manage users of specific type"""
    if user_type == "admin":
        users_df = get_all_admin_users()
        title = "Admin Users"
    else:
        users_df = get_all_users()
        title = "Regular Users"

    st.subheader(title)

    if not users_df.empty:
        # Display users table
        display_df = users_df[['username', 'email', 'full_name', 'created_at']].copy()
        display_df['created_at'] = pd.to_datetime(display_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(display_df)

        # Delete user section
        st.subheader("Delete User")
        usernames = users_df['username'].tolist()
        username_to_delete = st.selectbox("Select user to delete", usernames, key=f"delete_{user_type}")

        if st.button(f"Delete {user_type.title()}", key=f"btn_delete_{user_type}"):
            if username_to_delete == st.session_state.user['username']:
                st.error("Cannot delete your own account")
            else:
                success, message = delete_user(username_to_delete, user_type)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    else:
        st.info(f"No {user_type} users found")

def system_data_management():
    """System data management"""
    st.header("System Data Management")

    # Data generation
    st.subheader("Generate System Data")
    col1, col2 = st.columns(2)

    with col1:
        periods = st.slider("Number of days", 365, 365*5, 730)
        if st.button("Generate New Data"):
            with st.spinner("Generating data..."):
                data = generate_energy_data(periods=periods)
                data.to_csv('energy_data.csv', index=False)
                st.success("System data generated successfully!")

    with col2:
        if os.path.exists('energy_data.csv'):
            data = pd.read_csv('energy_data.csv')
            st.metric("Current Data Points", len(data))
            st.metric("Date Range", f"{data['date'].min()} to {data['date'].max()}")

    # Model training
    st.subheader("Model Training")
    if os.path.exists('energy_data.csv'):
        if st.button("Train System Model"):
            with st.spinner("Training model..."):
                data = pd.read_csv('energy_data.csv')
                data['date'] = pd.to_datetime(data['date'])
                X, y = prepare_data(data)
                model = train_model(X, y)
                save_model(model)
                st.success("Model trained successfully!")
    else:
        st.warning("No data available. Generate data first.")

def analytics_section():
    """Analytics and insights"""
    st.header("System Analytics")

    if os.path.exists('energy_data.csv'):
        data = pd.read_csv('energy_data.csv')
        data['date'] = pd.to_datetime(data['date'])

        # Basic analytics
        st.subheader("Data Analytics")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(data))
        with col2:
            st.metric("Avg Consumption", f"{data['consumption_kwh'].mean():.1f} kWh")
        with col3:
            st.metric("Date Range", f"{len(data)} days")

        # Consumption chart
        st.subheader("Consumption Trends")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data['date'], data['consumption_kwh'])
        ax.set_xlabel('Date')
        ax.set_ylabel('Consumption (kWh)')
        ax.set_title('System Energy Consumption Trends')
        st.pyplot(fig)

        # Model performance if available
        if os.path.exists('energy_model.pkl'):
            st.subheader("Model Performance")
            model = load_model()
            if model:
                X, y = prepare_data(data)
                if len(X) > 0:
                    split_idx = int(len(X) * 0.8)
                    X_test, y_test = X[split_idx:], y[split_idx:]
                    if len(X_test) > 0:
                        y_pred = model.predict(X_test)
                        mse = ((y_test - y_pred) ** 2).mean()
                        st.metric("Model MSE", f"{mse:.2f}")
                    else:
                        st.info("Not enough data for performance evaluation")
                else:
                    st.info("Model loaded but no test data available")
            else:
                st.warning("Could not load model")
        else:
            st.info("No trained model available")
    else:
        st.warning("No system data available for analytics")

if __name__ == "__main__":
    admin_dashboard()
