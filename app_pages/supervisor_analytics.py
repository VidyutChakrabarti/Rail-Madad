import streamlit as st
from auth.rbac_utils import require_role, get_department_complaints
from helperfunctions import get_department_statistics
import plotly.express as px
from collections import Counter
import pandas as pd

@require_role(['supervisor', 'admin'])
def show():
    user_dept = st.session_state.get('department')
    user_role = st.session_state.get('role')
    
    if user_role == 'admin':
        st.title("🎯 Admin - Supervisor Analytics")
        from vars import departments
        user_dept = st.selectbox("Select Department to View Analytics:", list(departments.keys()))
    else:
        st.title(f"📊 {user_dept} Department Analytics")
    
    if not user_dept:
        st.error("No department assigned to your account.")
        return
    
    # Get department data
    dept_complaints = get_department_complaints(user_dept)
    dept_stats = get_department_statistics(user_dept)
    
    # Overview metrics
    st.subheader("📈 Department Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Complaints", dept_stats['total_complaints'])
    col2.metric("Open", dept_stats['open_complaints'])
    col3.metric("In Progress", dept_stats['in_progress'])
    col4.metric("Resolved", dept_stats['resolved'])
    
    if dept_stats['total_complaints'] > 0:
        resolution_rate = (dept_stats['resolved'] / dept_stats['total_complaints']) * 100
        st.metric("Resolution Rate", f"{resolution_rate:.1f}%")
    
    st.divider()
    
    # Analytics charts
    if dept_complaints:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Priority Distribution")
            priority_counts = Counter([c.get('priority', 3) for c in dept_complaints])
            if priority_counts:
                fig1 = px.bar(
                    x=[f"Priority {p}" for p in sorted(priority_counts.keys())],
                    y=[priority_counts[p] for p in sorted(priority_counts.keys())],
                    title=f"{user_dept} - Priority Distribution",
                    color_discrete_sequence=['#FF6B6B']
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("📊 Status Distribution")
            status_counts = Counter([c.get('status', 'open') for c in dept_complaints])
            if status_counts:
                fig2 = px.pie(
                    values=list(status_counts.values()),
                    names=list(status_counts.keys()),
                    title=f"{user_dept} - Status Distribution"
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Team performance timeline (if dates available)
        st.subheader("📅 Complaint Timeline")
        date_counts = Counter([c.get('date_of_problem', 'Unknown') for c in dept_complaints])
        if date_counts:
            dates_df = pd.DataFrame(list(date_counts.items()), columns=['Date', 'Count'])
            dates_df = dates_df.sort_values('Date')
            fig3 = px.line(
                dates_df, 
                x='Date', 
                y='Count', 
                title=f"{user_dept} - Complaints Over Time",
                markers=True
            )
            fig3.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig3, use_container_width=True)
        
        # Priority vs Status matrix
        st.subheader("🔍 Priority vs Status Analysis")
        priority_status = {}
        for complaint in dept_complaints:
            priority = complaint.get('priority', 3)
            status = complaint.get('status', 'open')
            key = (priority, status)
            priority_status[key] = priority_status.get(key, 0) + 1
        
        if priority_status:
            matrix_data = []
            for (priority, status), count in priority_status.items():
                matrix_data.append({
                    'Priority': f"P{priority}",
                    'Status': status.title(),
                    'Count': count
                })
            
            matrix_df = pd.DataFrame(matrix_data)
            matrix_pivot = matrix_df.pivot(index='Priority', columns='Status', values='Count').fillna(0)
            st.dataframe(matrix_pivot, use_container_width=True)
    else:
        st.info(f"No complaints found for {user_dept} department to analyze.")

if __name__ == "__main__":
    show()
