import streamlit as st
from auth.rbac_utils import require_role, get_department_complaints
from helperfunctions import update_complaint_status, get_department_statistics
import plotly.express as px
from collections import Counter

@require_role(['staff', 'supervisor', 'admin'])
def show():
    user_dept = st.session_state.get('department')
    user_role = st.session_state.get('role')
    user_name = st.session_state.get('name')
    
    if user_role == 'admin':
        st.title("🎯 Admin - Department View")
        # Admin can select any department
        from vars import departments
        user_dept = st.selectbox("Select Department to View:", list(departments.keys()))
    else:
        st.title(f"💼 {user_dept} Department Dashboard")
    
    if not user_dept:
        st.error("No department assigned to your account.")
        return
    
    # Get department complaints
    dept_complaints = get_department_complaints(user_dept)
    dept_stats = get_department_statistics(user_dept)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Complaints", dept_stats['total_complaints'])
    col2.metric("Open", dept_stats['open_complaints'])
    col3.metric("In Progress", dept_stats['in_progress'])
    col4.metric("Resolved", dept_stats['resolved'])
    
    if dept_complaints:
        st.subheader("🚨 Priority Queue")
        
        priority_filter = st.selectbox("Filter by Priority", 
                                       ["All", "1 - Critical", "2 - Urgent", 
                                        "3 - Medium", "4 - Low", "5 - Very Low"])
        
        status_filter = st.selectbox("Filter by Status", 
                                     ["All", "open", "in_progress", "resolved", "closed"])
        
        filtered_complaints = dept_complaints
        if priority_filter != "All":
            priority_num = int(priority_filter[0])
            filtered_complaints = [c for c in filtered_complaints if c.get('priority') == priority_num]
        
        if status_filter != "All":
            filtered_complaints = [c for c in filtered_complaints if c.get('status', 'open') == status_filter]
        
        st.write(f"Showing {len(filtered_complaints)} complaints")
        
        for complaint in filtered_complaints:
            priority = complaint.get('priority', 3)
            priority_color = "🔴" if priority <= 2 else "🟡" if priority == 3 else "🟢"
            
            with st.expander(f"{priority_color} #{complaint['cno']} | Train: {complaint['train_number']} | Priority: {priority}"):
                # Display complaint details
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Passenger Email:** {complaint['mail']}")
                    st.write(f"**Date:** {complaint['date_of_problem']}")
                    st.write(f"**Current Status:** {complaint.get('status', 'open').title()}")
                    
                    # Show complaint text or issues
                    if complaint.get('complaint_text'):
                        st.write("**Complaint Text:**")
                        st.info(complaint['complaint_text'])
                    elif complaint.get('issues'):
                        st.write("**Issues:**")
                        issues = complaint['issues']
                        if isinstance(issues, list):
                            st.write(", ".join(issues))
                        else:
                            st.write(str(issues))
                
                with col2:
                    # Status update form (only for staff and above)
                    if user_role in ['staff', 'supervisor', 'admin']:
                        st.write("**Update Status:**")
                        current_status = complaint.get('status', 'open')
                        status_options = ["open", "in_progress", "resolved", "closed"]
                        try:
                            current_index = status_options.index(current_status)
                        except ValueError:
                            current_index = 0
                        
                        new_status = st.selectbox("Status", 
                                                 status_options,
                                                 index=current_index,
                                                 key=f"status_{complaint['cno']}")
                        
                        notes = st.text_area("Resolution Notes", 
                                           value=complaint.get('resolution_notes', ''),
                                           key=f"notes_{complaint['cno']}")
                        
                        if st.button("Update", key=f"btn_{complaint['cno']}"):
                            if update_complaint_status(complaint['cno'], new_status, notes, user_name, user_dept):
                                st.success("✅ Status updated!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update status")
        
        # Department analytics
        if user_role in ['supervisor', 'admin']:
            st.subheader("📊 Department Analytics")
            
            # Priority distribution
            priority_counts = Counter([c.get('priority', 3) for c in dept_complaints])
            if priority_counts:
                fig1 = px.bar(
                    x=[f"Priority {p}" for p in priority_counts.keys()],
                    y=list(priority_counts.values()),
                    title=f"{user_dept} Department - Priority Distribution"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            # Status distribution
            status_counts = Counter([c.get('status', 'open') for c in dept_complaints])
            if status_counts:
                fig2 = px.pie(
                    values=list(status_counts.values()),
                    names=list(status_counts.keys()),
                    title=f"{user_dept} Department - Status Distribution"
                )
                st.plotly_chart(fig2, use_container_width=True)
    
    else:
        st.info(f"No complaints found for {user_dept} department.")

if __name__ == "__main__":
    show()
