import streamlit as st
from auth.rbac_utils import require_role
from vars import *
from helperfunctions import *
import plotly.express as px
from collections import Counter
from datetime import date
import pandas as pd

@require_role(['admin', 'analyst'])
def show():
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
    labels, values = zip(*issue_counts.items()) if issue_counts else ([], [])
    if labels and values:
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
        dates = date_plotter()
        if dates:
            date_counts = Counter(dates)
            df = pd.DataFrame(list(date_counts.items()), columns=['Date', 'Count'])
            # Parse dates robustly: supports 'DD/MM/YYYY' and ISO 'YYYY-MM-DD'
            parsed_1 = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
            parsed_2 = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
            df['Date'] = parsed_1.fillna(parsed_2)
            if df['Date'].isna().all():
                st.warning("Could not parse dates")
            
            df = df.dropna()
            df = df.sort_values('Date')
            if not df.empty:
                fig = px.line(df, x='Date', y='Count', title='Complaints Registered Per Day',
                          labels={'Date': 'Date', 'Count': 'Number of Complaints',},
                          color_discrete_sequence=px.colors.sequential.Inferno,
                          markers=True)
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig)
            else:
                st.warning("No valid dates found")

if __name__ == "__main__":
    show()
