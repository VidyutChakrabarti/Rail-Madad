import os
import json
import ast
import streamlit as st
import random
import time 

file_path = 'log_file.json'

def all_logs(dep=None):
    """
    Fetch all complaints, optionally filtered by department(s).
    Now supports multi-department assignments.
    
    Args:
        dep: None (all), string (single dept), or list (multiple depts)
    
    Returns:
        List of complaints matching filter
    """
    with open(file_path, 'r') as file:
        complaints = json.load(file)
    
    all_comp = []
    
    for item in complaints:
        # If no filter, include all
        if dep is None:
            all_comp.append(item)
            continue
        
        # Convert single department to list for uniform handling
        filter_depts = [dep] if isinstance(dep, str) else dep
        
        # Check if complaint involves any of the filter departments
        complaint_depts = get_all_departments_for_complaint(item)
        
        if any(d in filter_depts for d in complaint_depts):
            all_comp.append(item)
    
    if len(all_comp) == 0:
        st.warning(f"No complaints found for department(s): {dep}")
        all_comp = complaints  # Show all if filter returns nothing
    
    return all_comp
    
def logger(log):
    """
    Logger function that handles complaint storage.
    For sub-complaints: simple storage with single 'department' field
    For backward compatibility: handles old multi-department format
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            my_list = json.load(file)
    else:
        my_list = []
    
    # If this is a sub-complaint, just store it as-is (no conversion needed)
    if log.get('is_sub_complaint', False):
        # Sub-complaints already have the correct format with single 'department'
        # No need to convert or add 'departments' field
        my_list.append(log)
        with open(file_path, 'w') as file:
            json.dump(my_list, file, indent=4)
        return
    
    # Handle backward compatibility for old formats
    # If old format with single 'department', convert to list for legacy code
    if 'department' in log and 'departments' not in log:
        # Only convert if not "Multi-Department" special case
        if log.get('department') != "Multi-Department":
            log['departments'] = [
                {
                    'department': log['department'],
                    'issues': log.get('issues', []),
                    'reasoning': 'Legacy single department assignment'
                }
            ]
    
    # For multi-department complaints, ensure 'department' field is set correctly
    if 'departments' in log and isinstance(log['departments'], list):
        if len(log['departments']) > 1:
            # For multi-department, keep "Multi-Department" as the department value
            if 'department' not in log:
                log['department'] = "Multi-Department"
    
    my_list.append(log)
    
    with open(file_path, 'w') as file:
        json.dump(my_list, file, indent=4)

def get_all_departments_for_complaint(complaint_data):
    """
    Extract all department names from a complaint's department assignments.
    Now handles sub-complaints with single department as well as multi-department format.
    
    Args:
        complaint_data: Complaint dict with 'departments' field or sub-complaint with single 'department' field
        
    Returns:
        List of department names
    """
    # Handle sub-complaints (they have 'is_sub_complaint' flag and single department)
    if complaint_data.get('is_sub_complaint', False):
        if 'department' in complaint_data:
            return [complaint_data['department']]
        else:
            return []
    
    # Handle multi-department format (departments field is a list of objects)
    if 'departments' in complaint_data and isinstance(complaint_data['departments'], list):
        return [dept['department'] for dept in complaint_data['departments']]
    elif 'department' in complaint_data:
        # Backward compatibility - single department
        return [complaint_data['department']]
    else:
        return []


def get_issues_for_department(complaint_data, department_name):
    """
    Get issues assigned to a specific department within a complaint.
    
    Args:
        complaint_data: Complaint dict
        department_name: Name of department
        
    Returns:
        List of issues for that department
    """
    if 'departments' in complaint_data:
        for dept_assignment in complaint_data['departments']:
            if dept_assignment['department'] == department_name:
                return dept_assignment.get('issues', [])
    return []

def plotter(train_number=None):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            logs = json.load(file)
        all_issues = []
        for item in logs:
            if train_number is None or item['train_number'] == train_number:
                # Handle issues extraction for sub-complaints
                if item.get('is_sub_complaint', False):
                    # Sub-complaints have issues as a list
                    issues = item.get('issues', [])
                    if isinstance(issues, list):
                        all_issues.extend(issues)
                    else:
                        try:
                            all_issues += ast.literal_eval(str(issues))
                        except:
                            all_issues.append(str(issues))
                else:
                    # Legacy format
                    try:
                        all_issues += ast.literal_eval(item['issues'])
                    except:
                        all_issues.append(item['issues'])
        if(len(all_issues) == 0):
            for item in logs:
                if item.get('is_sub_complaint', False):
                    issues = item.get('issues', [])
                    if isinstance(issues, list):
                        all_issues.extend(issues)
                    else:
                        try:
                            all_issues += ast.literal_eval(str(issues))
                        except:
                            all_issues.append(str(issues))
                else:
                    try:
                        all_issues += ast.literal_eval(item['issues'])
                    except:
                        all_issues.append(item['issues'])
            st.error("No Trains found.")
        return all_issues
    else:
        return ['Train Delay']
    
def pie_plotter():
    """
    Returns a list of all department assignments.
    Multi-department complaints contribute to multiple departments.
    Sub-complaints are also included.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            logs = json.load(file)
        
        all_departments = []
        for log in logs:
            # Handle sub-complaints (they have single department field)
            if log.get('is_sub_complaint', False):
                if 'department' in log:
                    all_departments.append(log['department'])
            # Check for new multi-department format
            elif 'departments' in log and isinstance(log['departments'], list):
                # Add each department from the assignment list
                for dept_assignment in log['departments']:
                    all_departments.append(dept_assignment['department'])
            elif 'department' in log:
                # Backward compatibility with old single-department format
                # Skip "Multi-Department" placeholder
                if log['department'] != "Multi-Department":
                    all_departments.append(log['department'])
        
        return all_departments if all_departments else ['Commercial', 'Medical']
    else:
        return ['Commercial', 'Medical']
    
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

def create_sub_complaints(original_complaint_data, department_assignments):
    """
    Create separate complaint entries for each department.
    ALL sub-complaints share the SAME complaint number (cno).
    
    Args:
        original_complaint_data: Original complaint dict with train details
        department_assignments: List of dept assignments from agent
        
    Returns:
        List of separate complaint entries with same cno
    """
    sub_complaints = []
    
    # Generate ONE complaint number that will be shared by all sub-complaints
    shared_cno = original_complaint_data.get('original_cno', generate_unique_id())
    
    for idx, dept_assignment in enumerate(department_assignments):
        # Create sub-complaint entry
        # All sub-complaints have the SAME cno
        sub_complaint = {
            "cno": shared_cno,  # Same complaint number for all
            "train_number": original_complaint_data['train_number'],
            "date_of_problem": original_complaint_data['date_of_problem'],
            "complaint_registered": original_complaint_data['complaint_registered'],
            "mail": original_complaint_data['mail'],
            "department": dept_assignment['department'],
            "complaint_text": dept_assignment.get('complaint_text', ''),  # Department-specific text
            "issues": dept_assignment['issues'],
            "priority": dept_assignment.get('priority_suggestion', 3),
            "status": "open",
            "is_sub_complaint": True
        }
        
        sub_complaints.append(sub_complaint)
    
    return sub_complaints
