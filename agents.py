from crewai import Agent

departments = ['finance', 'relations', 'food', 'bedding']

class Rail_agents():
    def department_routing_agent(self): 
        return Agent(
            role='Classifier', 
            goal='Classify the complaint to the most appropriate department.',
            backstory=f"""
            You are an expert in analyzing complaints and determining the best department to handle them. 
            Your task is to thoroughly analyze the text of each complaint and assign it to one of the following departments: 
            {departments}. Consider the nature of the complaint, the specific issues mentioned, and the expertise of each department.
            """,
            verbose=True,
            max_iter=15,
            allow_delegation=True
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
            allow_delegation=True
        )


