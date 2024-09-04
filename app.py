import streamlit as st
from vars import *
from main import crew, chatcrew 
from helperfunctions import *
import plotly.express as px
from collections import Counter

st.set_page_config(layout="wide")
pages = ["Home", "LiveChat", "Complaint Lodger"]
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
            st.write(response.raw)
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
        
        st.text_input('Email')
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
                inputs = {"complaint": complaint, "departments": departments}
                crew_output = crew.kickoff(inputs = inputs)
                st.write(crew_output.raw)
                log = {
                    'train_number': str(train_number),
                    'date': str(date),
                    'issues': crew_output.tasks_output[0].raw.strip("```json\n").strip("```").replace("\"", "'").replace("\\", "").replace("\n", "")
                }
                logger(log)