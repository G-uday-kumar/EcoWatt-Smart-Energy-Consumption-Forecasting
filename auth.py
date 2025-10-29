import pandas as pd
import os
import hashlib
import streamlit as st
from datetime import datetime

# File paths
USERS_FILE = 'users.xlsx'
ADMIN_USERS_FILE = 'admin_users.xlsx'

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_user_files():
    """Initialize user data files if they don't exist"""
    # Regular users file
    if not os.path.exists(USERS_FILE):
        users_df = pd.DataFrame(columns=['username', 'password', 'email', 'full_name', 'role', 'created_at'])
        # Add sample users
        sample_users = [
            {
                'username': 'user1',
                'password': hash_password('password123'),
                'email': 'user1@example.com',
                'full_name': 'John Doe',
                'role': 'user',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'username': 'user2',
                'password': hash_password('password123'),
                'email': 'user2@example.com',
                'full_name': 'Jane Smith',
                'role': 'user',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        users_df = pd.DataFrame(sample_users)
        users_df.to_excel(USERS_FILE, index=False)

    # Admin users file
    if not os.path.exists(ADMIN_USERS_FILE):
        admin_df = pd.DataFrame(columns=['username', 'password', 'email', 'full_name', 'role', 'created_at'])
        # Add sample admin
        sample_admin = [{
            'username': 'admin',
            'password': hash_password('admin123'),
            'email': 'admin@ecowatt.com',
            'full_name': 'System Administrator',
            'role': 'admin',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }]
        admin_df = pd.DataFrame(sample_admin)
        admin_df.to_excel(ADMIN_USERS_FILE, index=False)

def load_users():
    """Load regular users from Excel file"""
    if os.path.exists(USERS_FILE):
        return pd.read_excel(USERS_FILE)
    return pd.DataFrame(columns=['username', 'password', 'email', 'full_name', 'role', 'created_at'])

def load_admin_users():
    """Load admin users from Excel file"""
    if os.path.exists(ADMIN_USERS_FILE):
        return pd.read_excel(ADMIN_USERS_FILE)
    return pd.DataFrame(columns=['username', 'password', 'email', 'full_name', 'role', 'created_at'])

def save_users(users_df):
    """Save users to Excel file"""
    users_df.to_excel(USERS_FILE, index=False)

def save_admin_users(admin_df):
    """Save admin users to Excel file"""
    admin_df.to_excel(ADMIN_USERS_FILE, index=False)

def authenticate_user(username, password, user_type='user'):
    """Authenticate user login"""
    hashed_password = hash_password(password)

    if user_type == 'admin':
        users_df = load_admin_users()
    else:
        users_df = load_users()

    user = users_df[(users_df['username'] == username) & (users_df['password'] == hashed_password)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

def register_user(username, password, email, full_name, user_type='user'):
    """Register a new user"""
    if user_type == 'admin':
        users_df = load_admin_users()
    else:
        users_df = load_users()

    # Check if username already exists
    if username in users_df['username'].values:
        return False, "Username already exists"

    # Check if email already exists
    if email in users_df['email'].values:
        return False, "Email already exists"

    # Add new user
    new_user = {
        'username': username,
        'password': hash_password(password),
        'email': email,
        'full_name': full_name,
        'role': user_type,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)

    if user_type == 'admin':
        save_admin_users(users_df)
    else:
        save_users(users_df)

    return True, "Registration successful"

def get_all_users():
    """Get all regular users for admin view"""
    return load_users()

def get_all_admin_users():
    """Get all admin users"""
    return load_admin_users()

def delete_user(username, user_type='user'):
    """Delete a user"""
    if user_type == 'admin':
        users_df = load_admin_users()
    else:
        users_df = load_users()

    users_df = users_df[users_df['username'] != username]

    if user_type == 'admin':
        save_admin_users(users_df)
    else:
        save_users(users_df)

    return True, "User deleted successfully"
