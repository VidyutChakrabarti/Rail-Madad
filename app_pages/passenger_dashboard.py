import streamlit as st
from auth.rbac_utils import require_role, get_user_complaints
from helperfunctions import get_department_statistics
import plotly.express as px
from collections import Counter

@require_role(['passenger', 'admin'])
def show():
    st.title("🏠 Passenger Dashboard")
    st.markdown("### Welcome to Rail-Madad!")
    
    user_email = st.session_state.get('email')
    user_name = st.session_state.get('name')
    user_role = st.session_state.get('role')
    
    if user_role == 'admin':
        st.info("👨‍💼 Admin View: You can access all features from the Admin Dashboard.")
        user_email = st.text_input("View dashboard for email:", user_email)
    
    st.success(f"👋 Hello, {user_name}!")
    st.info("You can lodge complaints and track your submissions here.")
    
    # Get user's complaints
    my_complaints = get_user_complaints(user_email)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("My Complaints", len(my_complaints))
    col2.metric("Open", len([c for c in my_complaints if c.get('status', 'open') == 'open']))
    col3.metric("Resolved", len([c for c in my_complaints if c.get('status') == 'resolved']))
    
    if my_complaints:
        st.subheader("📊 My Complaint Status")
        
        # Status distribution
        status_counts = Counter([c.get('status', 'open') for c in my_complaints])
        if status_counts:
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="My Complaint Status Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent complaints
        st.subheader("📋 Recent Complaints")
        for complaint in my_complaints[-3:]:  # Last 3 complaints
            with st.expander(f"Complaint #{complaint['cno']} - {complaint.get('department', 'N/A')}"):
                st.write(f"**Train:** {complaint['train_number']}")
                st.write(f"**Date:** {complaint['date_of_problem']}")
                st.write(f"**Status:** {complaint.get('status', 'open').title()}")
                st.write(f"**Priority:** {complaint.get('priority', 'N/A')}")
    else:
        st.info("You haven't lodged any complaints yet. Use the 'Lodge Complaint' page to submit one.")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Lodge New Complaint", use_container_width=True):
            st.session_state.page = "complaint_lodger"
            st.rerun()
    with col2:
        if st.button("📋 View All My Complaints", use_container_width=True):
            st.session_state.page = "my_complaints"
            st.rerun()

if __name__ == "__main__":
    show()
