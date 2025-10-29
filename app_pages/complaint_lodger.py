import streamlit as st
from auth.rbac_utils import require_role
from vars import *
from main import crew
from helperfunctions import *
import json
import re

@require_role(['passenger', 'admin'])
def show():
    st.sidebar.markdown("\n\n\n")
    st.sidebar.image("complaint_agent.png")
    st.sidebar.markdown("\n\n\n")
    st.sidebar.write("Namaste 🙏, We are a group of AI agents operating on behalf of Indian Railways. Kindly, register your complaint here, we will route your issues to the correct authority and get back to you as soon as possible. Thank you.")
    st.markdown('<h2 class="gradient-text">File Your Grievance</h2>', unsafe_allow_html=True)
    
    # Pre-fill email if user is logged in
    user_email = st.session_state.get('email', '')
    
    with st.form(key='complaint_form'):
        c1, c2 = st.columns([1,2])
        with c1: 
            train_number = st.text_input('Train Number *')
        with c2: 
            date = st.date_input('Date *')
        
        mail = st.text_input('Email *', value=user_email)
        journey_details, pnr_no = st.columns([1, 1])
        with journey_details:
            st.selectbox('Journey Details', ['PNR','Seat number', 'Station Code'])
        with pnr_no:
            st.text_input('PNR No')
        
        type_, subtype = st.columns([1, 1])
        with type_:
            st.selectbox('Type', ['--Select--', 'Issue Type 1', 'Issue Type 2'])
        with subtype:
            st.selectbox('Sub Type', ['--Select--', 'Sub Type 1', 'Sub Type 2'])
        
        upload_file = st.file_uploader("Upload File", type=["jpg", "jpeg", "png", "pdf"], help='Select your file')
        
        complaint = st.text_area("Grievance Description *").strip()
        
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            if not train_number or not mail or not complaint:
                st.error("Please fill in all required fields (Train Number, Email, and Grievance Description)")
            else:
                st.success("Your complaint has been successfully submitted.")
                if len(complaint) > 0:
                    inputs = {"complaint": complaint, "departments": departments, "issue_department_mapping": issue_department_mapping}
                    crew_output = crew.kickoff(inputs = inputs)
                    
                    # Extract issues from Task 1 (Complaint Analysis)
                    issues_raw = crew_output.tasks_output[0].raw.strip("```json\n").strip("```").replace("\"", "'").replace("\\", "").replace("\n", "")
                    
                    # Extract department routing with sub-complaints from Task 2
                    try:
                        # Parse the multi-department assignment with complaint texts
                        dept_routing_raw = crew_output.tasks_output[1].raw
                        
                        # Remove markdown code blocks
                        if '```json' in dept_routing_raw:
                            # Extract content between ```json and ```
                            start_marker = '```json'
                            end_marker = '```'
                            start_idx = dept_routing_raw.find(start_marker) + len(start_marker)
                            end_idx = dept_routing_raw.rfind(end_marker)
                            if end_idx > start_idx:
                                dept_routing_cleaned = dept_routing_raw[start_idx:end_idx].strip()
                            else:
                                dept_routing_cleaned = dept_routing_raw
                        else:
                            dept_routing_cleaned = dept_routing_raw.strip()
                        
                        # Find JSON array boundaries (handle any extra text)
                        if '[' in dept_routing_cleaned and ']' in dept_routing_cleaned:
                            start_idx = dept_routing_cleaned.index('[')
                            end_idx = dept_routing_cleaned.rindex(']') + 1
                            dept_routing_cleaned = dept_routing_cleaned[start_idx:end_idx]
                        
                        # Try to handle JSON with literal newlines in string values
                        # First, try normal parsing
                        try:
                            dept_assignments = json.loads(dept_routing_cleaned)
                        except json.JSONDecodeError:
                            # If that fails, try replacing literal newlines with spaces
                            # Simple approach: join lines that look like string content
                            import io
                            cleaned_json = ""
                            in_string = False
                            i = 0
                            while i < len(dept_routing_cleaned):
                                char = dept_routing_cleaned[i]
                                if char == '"' and dept_routing_cleaned[max(0, i-1)] != '\\':
                                    in_string = not in_string
                                elif char == '\n' and in_string:
                                    cleaned_json += ' '  # Replace newlines in strings with spaces
                                else:
                                    cleaned_json += char
                                i += 1
                            
                            dept_assignments = json.loads(cleaned_json)
                        
                        # Ensure it's a list
                        if not isinstance(dept_assignments, list):
                            dept_assignments = [dept_assignments]
                        
                    except (json.JSONDecodeError, KeyError, IndexError) as e:
                        st.warning(f"Parsing error, attempting alternative approach: {e}")
                        
                        # Try to extract just the department names as fallback
                        try:
                            # Simple fallback: extract department names from the raw output
                            dept_pattern = r'"department"\s*:\s*"([^"]+)"'
                            departments_found = re.findall(dept_pattern, dept_routing_raw)
                            
                            if departments_found:
                                dept_assignments = []
                                for dept_name in departments_found:
                                    dept_assignments.append({
                                        "department": dept_name,
                                        "complaint_text": complaint,  # Use original complaint as fallback
                                        "issues": [issues_raw],
                                        "priority_suggestion": 3,
                                        "reasoning": "Parsed from agent output"
                                    })
                            else:
                                raise ValueError("No departments found")
                        except:
                            # Ultimate fallback: single department
                            dept_assignments = [{
                                "department": "Commercial",
                                "complaint_text": complaint,
                                "issues": [issues_raw],
                                "priority_suggestion": 3,
                                "reasoning": "Default assignment due to parsing error"
                            }]
                        
                        st.info("Using fallback parsing method.")
                    
                    # Generate master complaint number
                    master_cno = generate_unique_id()
                    
                    # Original complaint data
                    original_data = {
                        "original_cno": master_cno,
                        "train_number": str(train_number),
                        "date_of_problem": str(date),
                        "complaint_registered": str(date.today().strftime("%d/%m/%Y")),
                        "mail": str(mail)
                    }
                    
                    # Create sub-complaints for each department
                    sub_complaints = create_sub_complaints(original_data, dept_assignments)
                    
                    # Log each sub-complaint separately
                    for sub_complaint in sub_complaints:
                        logger(sub_complaint)
                    
                    # Display to user
                    st.success(f"✅ Complaint No: **{master_cno}**")
                    st.info(f"📋 Created **{len(sub_complaints)}** department-specific entries (ALL share the same Complaint No)")
                    
                    # Show each sub-complaint
                    with st.expander("📊 Department-Wise Entries", expanded=True):
                        st.write(f"**📌 All entries share Complaint No: {master_cno}**")
                        st.write("---")
                        for idx, sub in enumerate(sub_complaints, 1):
                            st.markdown(f"### {idx}. {sub['department']} Department")
                            st.write(f"**Priority:** {sub['priority']}")
                            if isinstance(sub['issues'], list):
                                st.write(f"**Issues:** {', '.join(sub['issues'])}")
                            else:
                                st.write(f"**Issues:** {sub['issues']}")
                            st.write(f"**Complaint Text:**")
                            st.info(sub['complaint_text'] if sub.get('complaint_text') else 'No specific complaint text provided.')
                            st.write("")
                    
                    # Show full AI response (Task 3/4 - Response letter)
                    with st.expander("📧 Full Response Letter", expanded=False):
                        st.write(crew_output.raw)

if __name__ == "__main__":
    show()
