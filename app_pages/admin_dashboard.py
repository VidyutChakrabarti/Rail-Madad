import streamlit as st
from auth.rbac_utils import require_role
from helperfunctions import all_logs, get_department_statistics
import plotly.express as px
from collections import Counter
import pandas as pd

@require_role(['admin'])
def show():
    st.title("🎯 System Administrator Dashboard")
    
    # Get all complaints and system stats
    all_complaints = all_logs()
    system_stats = get_department_statistics()
    
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Complaints", system_stats['total_complaints'])
    col2.metric("Open", system_stats['open_complaints'])
    col3.metric("In Progress", system_stats['in_progress'])
    col4.metric("Resolved", system_stats['resolved'])
    col5.metric("Avg Priority", system_stats['avg_priority'])
    
    st.divider()
    
    # System-wide visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 System-Wide Department Distribution")
        from helperfunctions import pie_plotter
        dept_data = pie_plotter()
        if dept_data:
            dept_counts = Counter(dept_data)
            fig_pie = px.pie(values=list(dept_counts.values()), 
                            names=list(dept_counts.keys()),
                            title="Complaints by Department")
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("📈 Priority Distribution")
        if all_complaints:
            priority_counts = Counter([c.get('priority', 3) for c in all_complaints])
            if priority_counts:
                fig_bar = px.bar(
                    x=[f"Priority {p}" for p in sorted(priority_counts.keys())],
                    y=[priority_counts[p] for p in sorted(priority_counts.keys())],
                    title="System-Wide Priority Distribution"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    if all_complaints:
        # Sort by complaint_registered date
        def sort_key(x):
            date_str = x.get('complaint_registered', '01/01/2024')
            try:
                # Try to parse DD/MM/YYYY format
                parts = date_str.split('/')
                if len(parts) == 3:
                    return (int(parts[2]), int(parts[1]), int(parts[0]))
            except:
                pass
            return (2024, 1, 1)
        
        recent_complaints = sorted(all_complaints, key=sort_key, reverse=True)[:5]
        
        for complaint in recent_complaints:
            with st.expander(f"#{complaint['cno']} - {complaint.get('department', 'N/A')} - {complaint.get('mail', 'N/A')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Train:** {complaint['train_number']}")
                    st.write(f"**Date:** {complaint['date_of_problem']}")
                    st.write(f"**Status:** {complaint.get('status', 'open').title()}")
                with col2:
                    st.write(f"**Priority:** {complaint.get('priority', 'N/A')}")
                    st.write(f"**Department:** {complaint.get('department', 'N/A')}")
                    st.write(f"**Registered:** {complaint.get('complaint_registered', 'N/A')}")
    
    # Department-wise breakdown
    st.subheader("🏢 Department-Wise Performance")
    
    from vars import departments
    dept_performance = []
    
    for dept_name in departments.keys():
        dept_stats = get_department_statistics(dept_name)
        if dept_stats['total_complaints'] > 0:
            resolution_rate = (dept_stats['resolved'] / dept_stats['total_complaints']) * 100
            dept_performance.append({
                'Department': dept_name,
                'Total': dept_stats['total_complaints'],
                'Open': dept_stats['open_complaints'],
                'In Progress': dept_stats['in_progress'],
                'Resolved': dept_stats['resolved'],
                'Resolution Rate %': round(resolution_rate, 1),
                'Avg Priority': dept_stats['avg_priority']
            })
    
    if dept_performance:
        df = pd.DataFrame(dept_performance)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export option
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Department Performance Report", 
                          csv, "department_performance.csv", "text/csv")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👥 Manage Users", use_container_width=True):
            st.info("User management feature coming soon! For now, edit auth/credentials.yaml directly.")
    
    with col2:
        if st.button("📊 Advanced Analytics", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    
    with col3:
        if st.button("📂 View All Complaints", use_container_width=True):
            st.session_state.page = "complaints_directory"
            st.rerun()

if __name__ == "__main__":
    show()
