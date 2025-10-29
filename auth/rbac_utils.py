import streamlit as st
from functools import wraps
from typing import List
import json

def require_role(allowed_roles: List[str]):
    """Decorator to restrict access based on user role"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if user is authenticated
            if 'authentication_status' not in st.session_state or \
               not st.session_state['authentication_status']:
                st.error("🔒 Please login to access this page")
                st.stop()
            
            # Check role
            if 'role' not in st.session_state:
                st.error("❌ Role not found. Please re-login.")
                st.stop()
            
            if st.session_state['role'] not in allowed_roles:
                st.error(f"⛔ Access Denied. Required role: {', '.join(allowed_roles)}")
                st.error(f"Your role: {st.session_state['role']}")
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_user_complaints(user_email: str):
    """Get complaints filed by specific user (for passengers)"""
    from helperfunctions import all_logs
    
    all_complaints = all_logs()
    user_complaints = [c for c in all_complaints if c.get('mail') == user_email]
    return user_complaints

def get_department_complaints(department: str):
    """Get complaints assigned to specific department (for staff/supervisor)"""
    from helperfunctions import all_logs, get_all_departments_for_complaint
    
    all_complaints = all_logs()
    dept_complaints = []
    
    for complaint in all_complaints:
        complaint_depts = get_all_departments_for_complaint(complaint)
        if department in complaint_depts:
            dept_complaints.append(complaint)
    
    return dept_complaints

def check_page_access(page_name: str, user_role: str) -> bool:
    """Check if user role has access to specific page"""
    
    access_matrix = {
        'home': ['admin', 'analyst'],  # Analytics dashboard - admin/analyst only
        'livechat': ['passenger', 'staff', 'supervisor', 'admin', 'analyst'],  # All roles
        'complaints_directory': ['admin', 'analyst'],  # All complaints - admin/analyst only
        'complaint_lodger': ['passenger', 'admin'],  # Lodge complaints - passengers/admin only
        'my_complaints': ['passenger', 'admin'],  # Own complaints - passengers only
        'staff_dashboard': ['staff', 'supervisor', 'admin'],  # Department complaints
        'admin_dashboard': ['admin'],  # Admin only
        'user_management': ['admin'],  # Admin only
    }
    
    return user_role in access_matrix.get(page_name, [])

def get_navigation_menu(role: str) -> List[str]:
    """Get navigation menu items based on user role"""
    
    menus = {
        'passenger': [
            "🏠 My Dashboard", 
            "📝 Lodge Complaint",
            "📋 My Complaints", 
            "💬 LiveChat"
        ],
        'staff': [
            "💼 Department Dashboard",
            "📊 My Complaints Queue",
            "💬 LiveChat"
        ],
        'supervisor': [
            "💼 Department Dashboard", 
            "📊 Department Analytics",
            "👥 Team Performance",
            "💬 LiveChat"
        ],
        'admin': [
            "🎯 Admin Dashboard",
            "🏠 System Analytics", 
            "📂 All Complaints",
            "👥 User Management",
            "📝 Lodge Complaint",
            "💬 LiveChat"
        ],
        'analyst': [
            "📊 Analytics Dashboard",
            "📂 All Complaints (Read-Only)",
            "📈 Trend Analysis", 
            "💬 LiveChat"
        ]
    }
    
    return menus.get(role, [])

def filter_complaints_by_role(complaints, user_role, user_email=None, user_department=None):
    """Filter complaints based on user role"""
    
    if user_role == 'passenger':
        # Passengers see only their own complaints
        return [c for c in complaints if c.get('mail') == user_email]
    
    elif user_role in ['staff', 'supervisor']:
        # Staff/Supervisors see only their department's complaints
        from helperfunctions import get_all_departments_for_complaint
        filtered = []
        for complaint in complaints:
            complaint_depts = get_all_departments_for_complaint(complaint)
            if user_department in complaint_depts:
                filtered.append(complaint)
        return filtered
    
    elif user_role in ['admin', 'analyst']:
        # Admin/Analysts see all complaints
        return complaints
    
    else:
        return []

