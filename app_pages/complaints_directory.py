import streamlit as st
from auth.rbac_utils import require_role
from vars import *
from helperfunctions import *
import requests
from streamlit_lottie import st_lottie
from datetime import date

@require_role(['admin', 'analyst'])
def show():
    url = requests.get( 
        "https://lottie.host/f4e79009-dce8-4792-9301-3c170d8bd054/jzWvnKQ6Xx.json") 
    url_json = dict() 
    if url.status_code == 200: 
        url_json = url.json() 
    else: 
        print("Error in the URL")
    
    st.sidebar.markdown('<h4 class="gradient-text">Complaints Directory</h4>', unsafe_allow_html=True)
    st.sidebar.markdown("Access all complaints filed till date using advanced filtering methods.")
    with st.sidebar: 
        st_lottie(url_json)
    
    def display_complaint_card(complaint):
        # Extract department info
        if 'departments' in complaint and isinstance(complaint['departments'], list):
            # Multi-department format
            dept_names = [d['department'] for d in complaint['departments']]
            dept_display = ', '.join(dept_names)
            
            # Create detailed department breakdown
            dept_details = "<br>".join([
                f"<span style='color:#9f0bfb'>• {d['department']}</span>: {', '.join(d.get('issues', []))}" 
                for d in complaint['departments']
            ])
        elif complaint.get('is_sub_complaint', False):
            # Sub-complaint format (single department with complaint_text)
            dept_display = complaint.get('department', 'N/A')
            
            # Show complaint text as details
            complaint_text = complaint.get('complaint_text', '')
            if complaint_text:
                dept_details = f"<span style='color:#9f0bfb'>• {dept_display}</span><br><i style='font-size:0.9em'>{complaint_text[:100]}...</i>"
            else:
                issues = complaint.get('issues', [])
                if isinstance(issues, list):
                    issues_str = ', '.join(issues)
                else:
                    issues_str = str(issues)
                dept_details = f"<span style='color:#9f0bfb'>• {dept_display}</span>: {issues_str}"
            
            # Show parent_cno if available
            if 'parent_cno' in complaint:
                dept_display += f" (Sub: {complaint['parent_cno']})"
        else:
            # Legacy single-department format
            dept_display = complaint.get('department', 'N/A')
            # Skip "Multi-Department" as it's just a placeholder
            if dept_display == "Multi-Department":
                dept_display = "Multiple Departments"
            
            # Try to get issues
            issues = complaint.get('issues', [])
            if isinstance(issues, str):
                issues_str = issues
            elif isinstance(issues, list):
                issues_str = ', '.join(issues)
            else:
                issues_str = str(issues)
            
            dept_details = f"<span style='color:#9f0bfb'>• {dept_display}</span>: {issues_str}"
        
        st.markdown(
            f'''
            <div class="card">
                <h4 style="font-family:'Playfair Display', serif">
                    <strong>Complaint Number:</strong> {complaint['cno']}
                </h4>
                <p>
                    <strong>Train Number:</strong> {complaint['train_number']}<br>
                    <strong>Department(s):</strong> {dept_display}<br>
                    <strong>Registered:</strong> {complaint['complaint_registered']}
                </p>
                <p><strong>Details:</strong><br>
                {dept_details}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    user_role = st.session_state.get('role')
    if user_role == 'analyst':
        st.info("👨‍💼 **Read-Only Mode**: You can view all complaints but cannot modify them.")
    
    with st.form(key='filters'):
        c1,c2 = st.columns([2,1])
        with c1:
            filter = st.multiselect("Filter by Department",list(departments.keys()))
        with c2:
            sort = st.selectbox("Sort by", ['Priority', 'Date of filing'])
        c1,c2,c3 = st.columns([1,1,1])
        with c1:
            train_filter = st.text_input("Filter by train_no.")
        with c2:
            ucid_filter = st.text_input("Filter by UCID")
        with c3: 
            date_range = st.slider("Filter by Date Range:", min_value=date(2024,9,1), max_value=date(2024,9,30), value=(date(2024,9,9), date(2024,9,21)))
        submit = st.form_submit_button("Apply Filters")
    
    logs = all_logs(filter if filter else None)
    
    # Apply additional filters
    if train_filter:
        logs = [c for c in logs if train_filter in str(c.get('train_number', ''))]
    
    if ucid_filter:
        logs = [c for c in logs if ucid_filter in str(c.get('cno', ''))]
    
    cols = st.columns(3)
    for i, complaint in enumerate(logs):
        with cols[i % 3]:
            display_complaint_card(complaint)

if __name__ == "__main__":
    show()
