import os 
import json
import ast

file_path = 'log_file.json'

def logger(log):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            my_list = json.load(file)
    else:
        my_list = []
    my_list.append(log)
    with open(file_path, 'w') as file:
        json.dump(my_list, file, indent=4)

def plotter(): 
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            l = json.load(file)
        all_issues = ['Train Delay']
        for item in l: 
            all_issues += ast.literal_eval(item['issues'])
        return all_issues
    else: 
        return []

