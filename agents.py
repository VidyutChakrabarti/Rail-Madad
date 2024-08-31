from crewai import Agent
from tools import *

import os
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
gemini_model_name = os.getenv('GEMINI_MODEL_NAME')
gemini_model = GoogleGenerativeAI(model=gemini_model_name, google_api_key=gemini_api_key)
from crewai_tools import (
   CodeInterpreterTool
)

codingtool = CodeInterpreterTool()
datetool = getCurrentDate

class Main_agents():
    def complaint_analysis_agent(self):
        return Agent(
            role='Analyzer',
            goal='Identify the main issue or topic of the complaint.',
            backstory="""You are an expert in analyzing railway related complaints to determine the primary issue or topic. 
            Your task is to thoroughly analyze the text of each complaint and identify the main issues, such as coach cleanliness, damage, staff behavior, etc.
            Consider the specific details mentioned in the complaint to accurately determine the main issues and summarize them under brief headings that encapsulate the issues. 
            Structure the headings into a json format and output it.  
            """,
            max_iter=15,
            verbose=True,
            llm=gemini_model,
            allow_delegation=False
        )
    
    def department_routing_agent(self): 
        return Agent(
            role='Classifier', 
            goal='Classify the complaint to the most appropriate department.',
            backstory="""You are an expert in analyzing railway related complaints and determining the best department to handle them. 
            Your task is to thoroughly analyze the list of issues provided and assign it to a department that can handle the most amount of issues.
            Consider the nature of the complaint, the specific issues mentioned, and the expertise of each department that are present in the dicitionary 'Departments'.
            """,
            verbose=True,
            max_iter=15,
            llm=gemini_model,
            allow_delegation=False
        )
    def scheduler(self):
        return Agent(
            role='Scheduler', 
            goal='Assign a priority rating based on the urgency with which a issue must be addressed by the railway departments.', 
            backstory="""You are an expert in evaluating a given complaint and assigning them a rating from 1 to 5 based on the urgency with which they must be addressed. 
            follow this rating system: 1. Critical (needs to be addressed immediately), 
            2. Urgent (must be addressed within a week but needs prior processing), 
            3. Medium (Important but urgent), 4. Low (non urgent but necessary) 5. Very Low(Optional or Long term), 
            When assigning the priority, take into account the department to which the complaint has been assigned and the prioirty it may have within that department.
            output must be in the form of ['Priority': 2]
            """,
            verbose=True,
            max_iter=15,
            llm=gemini_model,
            allow_delegation=False, 
        )
    def support_agent(self):
        return Agent(
            role="Senior Support Representative",
	        goal="Be the most friendly and helpful "
                "support representative in your team",
            backstory=(
        "You work at the indian railways, more specifically in the department assigned in the context."
        "You are tasked with providing support to a customer who has filed a complaint."
        "Make sure to address all the issues provided in the context and assure how the department is working on them."
        "Also make sure to include an expected time of hearing back based on the priority level assigned."
		"Be friendly and supportive and write your responses within 200 words."
		"Make sure to provide full complete answers, and make no assumptions."
            ),
            verbose=True,
            max_iter=10,
            llm=gemini_model,
            allow_delegation=False
        ) 
    def support_quality_assurance_agent(self):
        return Agent(
            role="Support Quality Assurance Specialist",
            	goal="Review the response provided by the support assistant and be the"
                " best support quality assurance in your department.",
                backstory=(
                "You work at Indian railways and "
                "are reviewing the responses from the support representative ensuring that "
                "the support representative is "
                "providing the best support possible.\n"
                "You need to make sure that the support representative "
                "is providing full, complete answers within 250 words strictly and makes no assumptions. "
                "Secondly, make sure the subject for the letter is personalized with extracted information from the complaint. "
                "If no personalization is possible then provide a generic subject. Thridly, ensure current date is mentioned. "
                "Output your response as a formal letter written that can be mailed immediately."
            ),
            allow_code_execution = False,
            verbose=True,
            max_iter=10,
            llm=gemini_model,
            tools = [datetool], 
            allow_delegation=True
        )
 
    
class Helper_agents():
    def video_analyser(self): 
        return Agent(
            llm=gemini_model,
        )
     
    def image_analysis_agent(self):
        return Agent(
            role='ImageEvaluator',
            goal='Generate a detailed description of the image, including any textual information extracted using OCR.',
            backstory="""You are an expert in analyzing images(mostly railway related) to generate detailed descriptions. 
            Your task is to thoroughly evaluate the visual content of each image and provide a comprehensive description. 
            If the image contains any text, use OCR to extract and include this textual information in your description.
            """,
            verbose=True,
            max_iter=10,
            llm=gemini_model,
            tools = [],
            allow_delegation=False
        )
    
    def meta_data_extractor(self):
        return Agent(
            llm=gemini_model,
        )

class ChatAgents(): 
    def chatagent(self): 
        return Agent(
            role = 'Chat Assitant', 
            goal = 'Provide the user with very specific information about his/her latest prompt.', 
            backstory = ("You are an expert in analyzing the prompt made by an user and giving a very specific reply that answers every query within the prompt in a very professional and brief manner. You are also an expert in extracting information from text recieved back from search tools. You must retrieve and take into account the history of chats before jumping to the response. Respond 'Sorry for the inconvenience but I can only answer Indian railways related questions.',if you feel the prompt is not related to railways. Do not use the tool more than once strictly."), 
            max_iter=5,
            llm=gemini_model,
            verbose = True, 
            tools = [search_internet],
            allow_delegation=True
        )
    
    
    


