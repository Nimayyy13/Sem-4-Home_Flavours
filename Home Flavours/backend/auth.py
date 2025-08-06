import streamlit as st
import hashlib
import streamlit_authenticator as stauth
from database import db
import pandas as pd

class AuthManager:
    def __init__(self):
        self.setup_session_state()
    
    def setup_session_state(self):
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'user_type' not in st.session_state:
            st.session_state.user_type = None
        if 'full_name' not in st.session_state:
            st.session_state.full_name = None
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        return self.hash_password(password) == hashed_password
    
    def register_user(self, username, email, password, full_name, phone, address, user_type='customer'):
        """Register a new user"""
        try:
            # Check if username or email already exists
            existing_user = db.execute_query(
                "SELECT id FROM users WHERE username = %s OR email = %s",
                (username, email)
            )
            
            if existing_user:
                return False, "Username or email already exists"
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Insert new user
            success = db.execute_update(
                """INSERT INTO users (username, email, password, full_name, phone, address, user_type) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (username, email, hashed_password, full_name, phone, address, user_type)
            )
            
            if success:
                return True, "Registration successful! Please login."
            else:
                return False, "Registration failed. Please try again."
                
        except Exception as e:
            return False, f"Error during registration: {str(e)}"
    
    def login_user(self, username, password):
        """Authenticate user login"""
        try:
            # Get user from database
            user = db.execute_query(
                "SELECT id, username, password, full_name, user_type FROM users WHERE username = %s",
                (username,)
            )
            
            if not user:
                return False, "Invalid username or password"
            
            user = user[0]
            
            # Verify password
            if self.verify_password(password, user['password']):
                # Set session state
                st.session_state.authenticated = True
                st.session_state.user_id = user['id']
                st.session_state.username = user['username']
                st.session_state.full_name = user['full_name']
                st.session_state.user_type = user['user_type']
                return True, "Login successful!"
            else:
                return False, "Invalid username or password"
                
        except Exception as e:
            return False, f"Error during login: {str(e)}"
    
    def logout_user(self):
        """Logout user and clear session"""
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.user_type = None
        st.session_state.full_name = None
        st.rerun()
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.authenticated
    
    def get_current_user(self):
        """Get current user information"""
        if self.is_authenticated():
            return {
                'id': st.session_state.user_id,
                'username': st.session_state.username,
                'full_name': st.session_state.full_name,
                'user_type': st.session_state.user_type
            }
        return None
    
    def require_auth(self, user_types=None):
        """Decorator to require authentication"""
        if not self.is_authenticated():
            st.error("Please login to access this page")
            st.stop()
        
        if user_types and st.session_state.user_type not in user_types:
            st.error("You don't have permission to access this page")
            st.stop()
    
    def show_login_form(self):
        """Display login form"""
        st.subheader("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if username and password:
                    success, message = self.login_user(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
        
        # Registration link
        st.markdown("---")
        st.markdown("Don't have an account? [Register here](#register)")
    
    def show_register_form(self):
        """Display registration form"""
        st.subheader("📝 Register")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
            
            with col2:
                full_name = st.text_input("Full Name")
                phone = st.text_input("Phone Number")
                address = st.text_area("Address")
                user_type = st.selectbox("User Type", ["customer", "tiffin_maker"])
            
            submit_button = st.form_submit_button("Register")
            
            if submit_button:
                if not all([username, email, password, confirm_password, full_name, phone, address]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = self.register_user(
                        username, email, password, full_name, phone, address, user_type
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

# Initialize auth manager
auth = AuthManager() 