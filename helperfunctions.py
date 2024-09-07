import os
import json
import ast
import streamlit as st
import random
file_path = 'log_file.json'

def all_logs():
    with open(file_path, 'r') as file:
        complaints = json.load(file)
        return complaints
    
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
            print("No trains found.")
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
