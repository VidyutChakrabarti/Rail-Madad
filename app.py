import streamlit as st
from vars import *
from main import crew, chatcrew 
from helperfunctions import *
import plotly.express as px
from collections import Counter
from datetime import date
import pandas as pd
import requests 
from streamlit_lottie import st_lottie 
import json
import re 

st.set_page_config(page_title='Rail-Madad', page_icon = "raillogo.png", layout = 'wide')

#st.set_page_config(layout="wide")
pages = ["Home", "LiveChat","Complaints Directory", "Complaint Lodger"]
page = st.sidebar.selectbox("Menu", pages, help="Navigate using this pane.")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": "Hi👋, How may I help you?"}]

if page == "Home":
    st.sidebar.markdown("\n\n\n")
    st.sidebar.image("raillogo.png")
    st.sidebar.markdown("\n\n\n")
    st.sidebar.write("For data analytics we provide you with dynamic plots based on insights extracted from complaints we received.")
    st.sidebar.write("1. Go to LiveChat to chat with our custom model.")
    st.sidebar.write("2. Visit Complaint lodger to file a complaint.")
    st.markdown('<h1 class="gradient-text">Welcome to Rail Madad</h1>', unsafe_allow_html=True)
    st.markdown("<hr class='gradient-line' />", unsafe_allow_html=True)  

    st.write("Filter by Train Number:")
    train_number_input = st.text_input("Enter Train Number to Filter", '')   
    all_issues = plotter(train_number_input if train_number_input else None)
    
    issue_counts = Counter(all_issues)
    labels, values = zip(*issue_counts.items())
    data = {'Issues': labels, 'Count': values}
    fig = px.bar(data, x='Issues', y='Count', title='Frequency of Issues', 
                 labels={'Issues': 'Issues', 'Count': 'Count'},
                 color='Issues', 
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)
    c1,c2 = st.columns([1,1])
    with c1:
        # Multi-department aware pie chart
        dep = pie_plotter()  # This now returns expanded department list

        # Count departments (some complaints may have multiple departments)
        department_counts = Counter(dep)
        labels, values = zip(*department_counts.items()) if department_counts else ([], [])

        if labels:
            data = {'Department': labels, 'Count': values}
            fig = px.pie(data, names='Department', values='Count', 
                         title='Complaints by Department (Multi-department complaints counted for each)',
                         color_discrete_sequence=px.colors.qualitative.Vivid)
            st.plotly_chart(fig)
            
            # Add info message
            st.info("📌 Note: Complaints assigned to multiple departments are counted once for each department.")
        else:
            st.warning("No complaint data available yet.")
    with c2: 
        date_counts = Counter(date_plotter())
        df = pd.DataFrame(list(date_counts.items()), columns=['Date', 'Count'])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        fig = px.line(df, x='Date', y='Count', title='Complaints Registered Per Day',
                  labels={'Date': 'Date', 'Count': 'Number of Complaints',},
                  color_discrete_sequence=px.colors.sequential.Inferno,
                  markers=True)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

  
elif page == "Complaints Directory":
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
    
    with st.form(key='filters'):
        c1,c2 = st.columns([2,1])
        with c1:
            filter = st.multiselect("Filter by Department",list(departments.keys()))
        with c2:
            sort = st.selectbox("Sort by", ['Priority', 'Date of filing'])
        c1,c2,c3 = st.columns([1,1,1])
        with c1:
            st.text_input("Filter by train_no.")
        with c2:
            st.text_input("Filter by UCID")
        with c3: 
            st.slider("Filter by Date Range:", min_value=date(2024,9,1), max_value=date(2024,9,30), value=(date(2024,9,9), date(2024,9,21)))
        submit = st.form_submit_button("Apply Filters")
    logs = all_logs(filter if filter else None)
    cols = st.columns(3)
    for i, complaint in enumerate(logs):
        with cols[i % 3]:
            display_complaint_card(complaint)
    
elif page == "LiveChat":
    st.sidebar.markdown("\n\n\n")
    st.markdown('<h1 class="gradient-text">Rail Madad AI Assitant</h1>', unsafe_allow_html=True)
    st.markdown("<hr class='gradient-line' />", unsafe_allow_html=True)
    st.sidebar.image("aibot.png")
    st.sidebar.markdown("\n\n\n")
    st.sidebar.write("Namaste 🙏, I am the Rail madad AI chatbot. Ask me any questions about Indian Railways and i will give you real time info for all of them. Thank you.")
    for msg in st.session_state['messages']: 
         with st.chat_message(msg["role"]):
              st.write(msg["content"]) 

    prompt = st.chat_input("Ask anything about Indian railways...")
    if prompt: 
        with st.chat_message("user"):
            st.write(prompt)

        inputs = {'prompt': prompt, 'history': st.session_state['messages'][:-4]} 
        response = chatcrew.kickoff(inputs = inputs)

        st.session_state['messages'].append({"role":"user","content": prompt})
        with st.chat_message("assistant"):
            st.write_stream(word_generator(response.raw))
        st.session_state['messages'].append({"role": "assistant", "content": response.raw})
        

elif page == "Complaint Lodger":
    st.sidebar.markdown("\n\n\n")
    st.sidebar.image("complaint_agent.png")
    st.sidebar.markdown("\n\n\n")
    st.sidebar.write("Namaste 🙏, We are a group of AI agents operating on behalf of Indian Railways. Kindly, register your complaint here, we will route your issues to the correct authority and get back to you as soon as possible. Thank you.")
    st.markdown('<h2 class="gradient-text">File Your Grievance</h2>', unsafe_allow_html=True)
    
    with st.form(key='complaint_form'):
        c1, c2 = st.columns([1,2])
        with c1: 
            train_number = st.text_input('Train Number *')
        with c2: 
            date = st.date_input('Date *')
        
        mail = st.text_input('Email *')
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