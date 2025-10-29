import streamlit as st
import yaml
from yaml.loader import SafeLoader
from auth.rbac_utils import get_navigation_menu, check_page_access
import subprocess
import sys
import os

# Page config
st.set_page_config(
    page_title="Rail-Madad | AI-Powered Complaint Management",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load authentication config
@st.cache_resource
def load_config():
    try:
        # Primary credentials file
        if os.path.exists('auth/credentials.yaml'):
            with open('auth/credentials.yaml') as file:
                return yaml.load(file, Loader=SafeLoader)
        # Fallback to example template for collaborators
        example_path = 'auth/credentials_example.yaml'
        if os.path.exists(example_path):
            st.info("Using example credentials from auth/credentials_example.yaml. Create auth/credentials.yaml for your local setup.")
            with open(example_path) as file:
                return yaml.load(file, Loader=SafeLoader)
        raise FileNotFoundError('auth/credentials.yaml not found')
    except FileNotFoundError:
        st.error("❌ Authentication configuration file not found!")
        st.error("Please create auth/credentials.yaml file (you can copy from auth/credentials_example.yaml).")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading authentication config: {e}")
        st.stop()

config = load_config()

def verify_demo_password(input_password: str, stored_password: str) -> bool:
    # Accept demo password 'test123' for repo users, or allow plaintext match for custom setups
    if input_password == 'test123':
        return True
    return stored_password and input_password == stored_password

# Login UI
authentication_status = st.session_state.get('authentication_status')
username = st.session_state.get('username')
name = st.session_state.get('name')

if authentication_status is None or not authentication_status:
    st.markdown('<h1 class="gradient-text">Welcome to Rail-Madad AI 🚂</h1>', unsafe_allow_html=True)
    st.markdown("<hr class='gradient-line' />", unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        input_username = st.text_input("Username")
        input_password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in")

    if submitted:
        user_db = config.get('credentials', {}).get('usernames', {})
        user_record = user_db.get(input_username)
        if user_record and verify_demo_password(input_password, user_record.get('password', '')):
            st.session_state['authentication_status'] = True
            st.session_state['username'] = input_username
            st.session_state['name'] = user_record.get('name', input_username)
            st.session_state['email'] = user_record.get('email', input_username)
            st.session_state['role'] = user_record.get('role')
            st.session_state['department'] = user_record.get('department')
            authentication_status = True
            username = input_username
            name = st.session_state['name']
            st.success("Signed in successfully")
            st.rerun()
        else:
            authentication_status = False
            st.error('❌ Username/password is incorrect')

if authentication_status:
    # Get user details
    user_data = config['credentials']['usernames'][username]
    user_role = user_data['role']
    user_name = user_data['name']
    user_email = user_data.get('email', username)
    user_dept = user_data.get('department', None)
    
    # Store in session state
    st.session_state['authentication_status'] = True
    st.session_state['username'] = username
    st.session_state['name'] = user_name
    st.session_state['email'] = user_email
    st.session_state['role'] = user_role
    st.session_state['department'] = user_dept
    
    # Initialize messages for LiveChat if not exists
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "assistant", "content": "Hi👋, How may I help you?"}]
    
    # Sidebar
    with st.sidebar:
        st.title(f"Welcome, {user_name}! 👋")
        st.info(f"**Role:** {user_role.title()}")
        if user_dept:
            st.info(f"**Department:** {user_dept}")
        
        st.divider()
        
        # Navigation based on role
        st.subheader("📌 Navigation")
        
        if user_role == 'passenger':
            if st.button("🏠 My Dashboard", use_container_width=True):
                st.session_state.page = "passenger_dashboard"
                st.rerun()
            if st.button("📝 Lodge Complaint", use_container_width=True):
                st.session_state.page = "complaint_lodger"
                st.rerun()
            if st.button("📋 My Complaints", use_container_width=True):
                st.session_state.page = "my_complaints"
                st.rerun()
            if st.button("💬 LiveChat", use_container_width=True):
                st.session_state.page = "livechat"
                st.rerun()
        
        elif user_role == 'staff':
            if st.button("💼 Department Dashboard", use_container_width=True):
                st.session_state.page = "staff_dashboard"
                st.rerun()
            if st.button("💬 LiveChat", use_container_width=True):
                st.session_state.page = "livechat"
                st.rerun()
        
        elif user_role == 'supervisor':
            if st.button("💼 Department Dashboard", use_container_width=True):
                st.session_state.page = "staff_dashboard"
                st.rerun()
            if st.button("📊 Department Analytics", use_container_width=True):
                st.session_state.page = "supervisor_analytics"
                st.rerun()
            if st.button("💬 LiveChat", use_container_width=True):
                st.session_state.page = "livechat"
                st.rerun()
        
        elif user_role == 'admin':
            if st.button("🎯 Admin Dashboard", use_container_width=True):
                st.session_state.page = "admin_dashboard"
                st.rerun()
            if st.button("🏠 System Analytics", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()
            if st.button("📂 All Complaints", use_container_width=True):
                st.session_state.page = "complaints_directory"
                st.rerun()
            if st.button("📝 Lodge Complaint", use_container_width=True):
                st.session_state.page = "complaint_lodger"
                st.rerun()
            if st.button("💬 LiveChat", use_container_width=True):
                st.session_state.page = "livechat"
                st.rerun()
        
        elif user_role == 'analyst':
            if st.button("📊 Analytics Dashboard", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()
            if st.button("📂 All Complaints (Read-Only)", use_container_width=True):
                st.session_state.page = "complaints_directory"
                st.rerun()
            if st.button("💬 LiveChat", use_container_width=True):
                st.session_state.page = "livechat"
                st.rerun()
        
        st.divider()
        
        # Logout button
        if st.button('Logout', use_container_width=True):
            for key in ['authentication_status','username','name','email','role','department','page','messages']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Initialize page if not set
    if 'page' not in st.session_state:
        if user_role == 'passenger':
            st.session_state.page = "passenger_dashboard"
        elif user_role in ['staff', 'supervisor']:
            st.session_state.page = "staff_dashboard"
        elif user_role == 'admin':
            st.session_state.page = "admin_dashboard"
        elif user_role == 'analyst':
            st.session_state.page = "home"
    
    # Route to pages based on selection
    try:
        if st.session_state.page == "passenger_dashboard":
            from app_pages import passenger_dashboard
            passenger_dashboard.show()
        
        elif st.session_state.page == "complaint_lodger":
            from app_pages import complaint_lodger
            complaint_lodger.show()
        
        elif st.session_state.page == "my_complaints":
            from app_pages import my_complaints
            my_complaints.show()
        
        elif st.session_state.page == "livechat":
            from app_pages import livechat
            livechat.show()
        
        elif st.session_state.page == "staff_dashboard":
            from app_pages import staff_dashboard
            staff_dashboard.show()
        
        elif st.session_state.page == "supervisor_analytics":
            from app_pages import supervisor_analytics
            supervisor_analytics.show()
        
        elif st.session_state.page == "admin_dashboard":
            from app_pages import admin_dashboard
            admin_dashboard.show()
        
        elif st.session_state.page == "home":
            # Import and run original analytics dashboard
            from app_pages import analytics_dashboard
            analytics_dashboard.show()
        
        elif st.session_state.page == "complaints_directory":
            from app_pages import complaints_directory
            complaints_directory.show()
    except ImportError as e:
        st.error(f"❌ Error importing page module: {e}")
        st.info("Please ensure all page modules are created in the pages/ folder.")
    except Exception as e:
        st.error(f"❌ Error loading page: {e}")
        import traceback
        st.code(traceback.format_exc())

elif authentication_status == False:
    st.error('❌ Username/password is incorrect')
    
    # Show demo credentials
    with st.expander("🔑 Demo Credentials"):
        st.markdown("""
        **Test Accounts (password for all: `test123`):**
        
        | Role | Username | Access Level |
        |------|----------|--------------|
        | **Admin** | `admin1` | Full system access |
        | **Analyst** | `analyst1` | Read-only analytics |
        | **Supervisor** | `supervisor_commercial` | Commercial dept management |
        | **Staff** | `staff_commercial` | Commercial dept complaints |
        | **Passenger** | `passenger1` | Own complaints only |
        """)

elif authentication_status == None:
    st.warning('⚠️ Please enter your username and password')
    
    # Welcome message
    st.markdown('<h1 class="gradient-text">Welcome to Rail-Madad AI 🚂</h1>', unsafe_allow_html=True)
    st.markdown("<hr class='gradient-line' />", unsafe_allow_html=True)
    
    st.info("""
    ### Intelligent Railway Complaint Management System
    
    **Features:**
    - 🤖 AI-powered multi-department routing
    - 👥 Role-based access control
    - 📊 Real-time analytics and insights
    - 💬 Live chat with AI assistant
    - 📈 Department-wise performance tracking
    """)
    
    # Show demo credentials
    with st.expander("🔑 Demo Credentials for Testing"):
        st.markdown("""
        **All test accounts use password:** `test123`
        
        | Role | Username | What You Can See |
        |------|----------|------------------|
        | **Admin** | `admin1` | Everything - full system control |
        | **Analyst** | `analyst1` | All analytics (read-only) |
        | **Supervisor** | `supervisor_commercial` | Commercial department analytics |
        | **Staff** | `staff_commercial` | Commercial complaints only |
        | **Passenger** | `passenger1` | Own complaints + lodge new ones |
        """)
