import streamlit as st
from vars import *
from main import crew 
st.set_page_config(layout="wide")
pages = ["Home", "LiveChat","Complaint Lodger"]
page = st.sidebar.selectbox("Menu", pages)

if page == "Home":
    st.title("Welcome to Rail Madad.")
    st.write("1. Go to LiveChat to chat with our custom model.")
    st.write("2. Visit Complaint lodger to file a complaint.")

elif page == "LiveChat":
    st.title("Chatting interface")
    st.write("Fine tuned agent will have tools such as the serper tool to allow real time access to train timings and Railway information.")

elif page == "Complaint Lodger":
    st.header("Submit your complaint here.")
    with st.form(key='complaint_form', clear_on_submit=True): 
        complaint = st.text_area("Enter your message here:").strip() 
        uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button(label='Submit') 
    if submit: 
        st.success("Your complaint has been successfully submitted.")
        if(len(complaint)>0):
            inputs = {"complaint": complaint, "departments": departments}
            crew_output = crew.kickoff(inputs = inputs)
            print(crew_output.raw)
