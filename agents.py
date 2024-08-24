from crewai import Agent
from tools import *

#initializing tools
ocr_tool = OCRTool()


class Main_agents:
    def department_routing_agent(self): 
        return Agent(
            role='Classifier', 
            goal='Classify the complaint to the most appropriate department.',
            backstory=f"""
            You are an expert in analyzing complaints and determining the best department to handle them. 
            Your task is to thoroughly analyze the text of each complaint and assign it to one of the departments.
            Consider the nature of the complaint, the specific issues mentioned, and the expertise of each department.
            """,
            verbose=True,
            max_iter=15,
            allow_delegation=False
        )
    def complaint_analysis_agent(self):
        return Agent(
            role='Analyzer',
            goal='Identify the main issue or topic of the complaint.',
            backstory=f"""
            You are an expert in analyzing complaints to determine the primary issue or topic. 
            Your task is to thoroughly analyze the text of each complaint and identify the main issue, such as coach cleanliness, damage, staff behavior, etc.
            Consider the specific details mentioned in the complaint to accurately determine the main issue and summarize it within one sentence at most. 
            """,
            verbose=True,
            max_iter=15,
            allow_delegation=False
        )
    def scheduler(self):
        return Agent(
            
        )
    def writer(self):
        return Agent(

        ) 
    def editor(self):
        return Agent(

        )
 
    
class Helper_agents:
    def video_analyser(self): 
        return Agent(

        )
     
    def image_analysis_agent(self):
        return Agent(
            role='ImageEvaluator',
            goal='Generate a detailed description of the image, including any textual information extracted using OCR.',
            backstory=f"""
            You are an expert in analyzing images to generate detailed descriptions. 
            Your task is to thoroughly evaluate the visual content of each image and provide a comprehensive description. 
            If the image contains any text, use OCR to extract and include this textual information in your description.
            """,
            verbose=True,
            max_iter=15,
            tools = [ocr_tool],
            allow_delegation=False
        )
    
    def meta_data_extractor(self):
        return Agent(

        )
    
    


