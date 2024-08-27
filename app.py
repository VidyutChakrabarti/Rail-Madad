import streamlit as st
from vars import *
from main import crew, chatcrew 
from helperfunctions import *
import plotly.express as px
from collections import Counter
st.set_page_config(layout="wide")
pages = ["Home", "LiveChat","Complaint Lodger"]
page = st.sidebar.selectbox("Menu", pages)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True) 

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": "Hi👋, How may I help you?"}]

if page == "Home":
    st.markdown('<h1 class="gradient-text">Welcome to Rail Madad</h1>', unsafe_allow_html=True)
    st.write("1. Go to LiveChat to chat with our custom model.")
    st.write("2. Visit Complaint lodger to file a complaint.")
    all_issues = plotter()
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
    for msg in st.session_state['messages']: 
         with st.chat_message(msg["role"]):
              st.write(msg["content"]) 

    prompt = st.chat_input("Ask anything about Indian railways...")
    if prompt: 
        with st.chat_message("user"):
            st.write(prompt)

        inputs = {'prompt': prompt,'history': st.session_state['messages']} 
        response = chatcrew.kickoff(inputs = inputs)

        st.session_state['messages'].append({"role":"user","content": prompt})
        with st.chat_message("assistant"):
            st.write(response.raw)
        st.session_state['messages'].append({"role": "assistant", "content": response.raw})
        

elif page == "Complaint Lodger":
    st.header("Submit your complaint here.")
    with st.form(key='complaint_form', clear_on_submit=True):
        c1, c2 = st.columns([1,2]) 
        with c1: 
            train_number = st.text_input('Train Number')
        with c2: 
            date = st.date_input('Date')
        complaint = st.text_area("Enter your message here:").strip() 
        uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button(label='Submit') 
    if submit: 
        st.success("Your complaint has been successfully submitted.")
        if(len(complaint)>0):
            inputs = {"complaint": complaint, "departments": departments}
            crew_output = crew.kickoff(inputs = inputs)
            st.write(crew_output.raw)
            log = {'train_number': str(train_number), 'date': str(date), 'issues': crew_output.tasks_output[0].raw.strip("```json\n").strip("\n```").replace("\"", "'").replace("\\", "")}
            logger(log)
        
