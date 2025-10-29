from crewai import Agent
from tools import *
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
import os

# Load model configuration from Streamlit secrets or environment variables
def _get_secret(path_keys, env_key, default=None):
    try:
        # Navigate nested keys in st.secrets like ['api_keys', 'GEMINI_API_KEY']
        value = st.secrets
        for key in path_keys:
            value = value[key]
        if value:
            return value
    except Exception:
        pass
    return os.getenv(env_key, default)

gemini_api_key = _get_secret(['api_keys', 'GEMINI_API_KEY'], 'GEMINI_API_KEY')
gemini_model_name = _get_secret(['model', 'GEMINI_MODEL_NAME'], 'GEMINI_MODEL_NAME', default='gemini-1.5-pro')

# Initialize model lazily and avoid halting the whole app on import
gemini_model = None
if gemini_api_key:
    gemini_model = GoogleGenerativeAI(model=gemini_model_name, google_api_key=gemini_api_key)
else:
    st.warning("GEMINI_API_KEY not set. AI features will be disabled until configured.")
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
            role='Multi-Department Sub-Complaint Generator',
            goal='Create separate complaint assignments for each relevant department with department-specific complaint text.',
            backstory="""You are an expert in analyzing railway complaints and 
            creating department-specific sub-complaints. Your task is to:
            
            1. IDENTIFY: Analyze the complaint and identify ALL distinct issues
            2. CATEGORIZE: Determine which department handles each issue
            3. GENERATE: Write a SEPARATE complaint text for EACH department
               - Each department gets ONLY the text relevant to their issues
               - Rewrite in professional language specific to that department
               - Include context but focus on their specific problems
            4. ROUTE: Assign each sub-complaint to its department
            
            CRITICAL RULES:
            - If complaint has AC issue + staff issue → Create TWO separate complaints
            - AC complaint text should ONLY mention AC problem (for Mechanical)
            - Staff complaint text should ONLY mention staff behavior (for Commercial)
            - Each department gets a STANDALONE, COMPLETE complaint description
            - Do NOT just split issues - REWRITE complaint text for each department
            
            EXAMPLE:
            Original: "AC was not working and when I complained, the staff was very rude"
            
            Output TWO Sub-Complaints:
            1. Mechanical Department:
               Complaint Text: "The air conditioning system in my coach was completely 
               non-functional throughout the journey, causing significant discomfort 
               in the hot weather."
            
            2. Commercial Department:
               Complaint Text: "When I approached the train staff to report an issue, 
               they responded in a very rude and unprofessional manner, refusing to 
               assist me."
            
            Each department sees ONLY their relevant complaint with full context.""",
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
                "If no personalization is possible then provide a generic subject. Thirdly, ensure current date is mentioned in DD/MM/YYYY format. "
                "Output your response as a formal letter written that can be mailed immediately."
            ),
            allow_code_execution = False,
            verbose=True,
            max_iter=15,
            llm=gemini_model,
            tools = [], 
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
    
    
    


