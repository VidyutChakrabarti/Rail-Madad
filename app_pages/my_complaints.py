import streamlit as st
from auth.rbac_utils import require_role, get_user_complaints

@require_role(['passenger', 'admin'])
def show():
    st.title("📋 My Complaints")
    
    user_email = st.session_state.get('email')
    user_role = st.session_state.get('role')
    
    if user_role == 'admin':
        # Admin can view any user's complaints
        st.info("👨‍💼 Admin View: You can see all complaints. Use 'All Complaints' for full system view.")
        user_email = st.text_input("View complaints for email:", user_email)
    
    my_complaints = get_user_complaints(user_email)
    
    if len(my_complaints) == 0:
        st.info("No complaints found for this user.")
        if user_role == 'passenger':
            st.markdown("👉 Use the **Lodge Complaint** page to submit a new complaint")
    else:
        st.success(f"Found {len(my_complaints)} complaint(s)")
        
        # Filters
        status_filter = st.selectbox("Filter by Status", 
                                      ["All", "open", "in_progress", "resolved", "closed"])
        
        # Display complaints
        for idx, complaint in enumerate(my_complaints):
            if status_filter != "All" and complaint.get('status', 'open') != status_filter:
                continue
            
            with st.expander(f"🎫 Complaint #{complaint['cno']} - Train {complaint['train_number']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Train Number:** {complaint['train_number']}")
                    st.write(f"**Date of Problem:** {complaint['date_of_problem']}")
                    st.write(f"**Filed On:** {complaint.get('complaint_registered', 'N/A')}")
                    st.write(f"**Email:** {complaint.get('mail', 'N/A')}")
                
                with col2:
                    status = complaint.get('status', 'open')
                    if status == 'resolved':
                        st.success(f"**Status:** ✅ {status.title()}")
                    elif status == 'in_progress':
                        st.info(f"**Status:** ⏳ {status.title()}")
                    else:
                        st.warning(f"**Status:** 🔴 {status.title()}")
                    
                    st.write(f"**Department:** {complaint.get('department', 'N/A')}")
                    st.write(f"**Priority:** {complaint.get('priority', 'N/A')}")
                
                st.divider()
                
                # Show complaint text or issues
                if complaint.get('complaint_text'):
                    st.write("**Complaint Details:**")
                    st.info(complaint['complaint_text'])
                elif complaint.get('issues'):
                    st.write("**Issues Reported:**")
                    issues = complaint['issues']
                    if isinstance(issues, list):
                        st.write(", ".join(issues))
                    else:
                        st.write(str(issues))
                
                if complaint.get('resolution_notes'):
                    st.write("**Resolution Notes:**")
                    st.success(complaint['resolution_notes'])
                
                if complaint.get('updated_by'):
                    st.write(f"*Last updated by: {complaint['updated_by']}*")

if __name__ == "__main__":
    show()
