import os
import json
import ast
import streamlit as st
import random
import time 

file_path = 'log_file.json'

def all_logs(dep=None):
    with open(file_path, 'r') as file:
        complaints = json.load(file)
        all_comp = []
        for item in complaints:
            if dep is None or item['department'] in dep:
                all_comp.append(item)
        
        if len(all_comp) == 0:
            st.warning("No complaints found for this department.")
            all_comp = complaints
        return all_comp
    
def logger(log):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            my_list = json.load(file)
    else:
        my_list = []
    my_list.append(log)
    with open(file_path, 'w') as file:
        json.dump(my_list, file, indent=4)

def plotter(train_number=None):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            logs = json.load(file)
        all_issues = []
        for item in logs:
            if train_number is None or item['train_number'] == train_number:
                all_issues += ast.literal_eval(item['issues'])
        if(len(all_issues) == 0):
            for item in logs:
                all_issues += ast.literal_eval(item['issues'])
            st.error("No Trains found.")
        return all_issues
    else:
        return ['Train Delay']
    
def pie_plotter():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            logs = json.load(file)
        departments = [log['department'] for log in logs]
        return departments
    else: 
        return ['Commercial','Medical']
    
def date_plotter():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            logs = json.load(file)
        dates = [log['date_of_problem'] for log in logs]
        return dates
    else: 
        return ['12-09-2024', '14-09-2024']

def generate_unique_id(length=9):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def word_generator(text, delay:float=0.07):
    for word in text.split(): 
        yield word + ' '
        time.sleep(delay)
