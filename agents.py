from crewai import Agent

departments = {
    'Engineering': "Responsible for the construction and maintenance of railway tracks, bridges, and buildings.",
    'Mechanical': "Manages the maintenance and operation of locomotives, coaches, and wagons.",
    'Electrical': "Handles the electrification of railway lines and the maintenance of electrical equipment.",
    'Traffic': "Oversees the operation of trains, including scheduling and control.",
    'Commercial': "Manages passenger services, ticketing, and freight operations.",
    'Personnel': "Deals with human resources, including recruitment, training, and employee welfare.",
    'Finance': "Responsible for budgeting, accounting, and financial management.",
    'Signal and Telecommunication': "Maintains signaling systems and communication networks.",
    'Stores': "Manages the procurement and distribution of materials and supplies.",
    'Safety': "Ensures the safety of railway operations and implements safety protocols.",
    'Security': "The Railway Protection Force (RPF) is responsible for the security of railway property and passengers.",
    'Medical': "Provides healthcare services to railway employees and their families.",
    'Legal': "Handles legal matters and litigation involving Indian Railways.",
    'Public Relations': "Manages communication with the public and media."
}

class Main_agents():
    def department_routing_agent(self): 
        return Agent(
            role='Classifier', 
            goal='Classify the complaint to the most appropriate department.',
            backstory=f"""
            You are an expert in analyzing complaints and determining the best department to handle them. 
            Your task is to thoroughly analyze the text of each complaint and assign it to one of the following departments given with their description: 
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
    def scheduler(self):
        return Agent(

        )
    def writer(self):
        return Agent(

        ) 
    def editor(self):
        return Agent(

        )
 
    
class Helper_agents():
    def video_analyser(self): 
        return Agent(

        ) 
    def image_analyzer(self): 
        return Agent(

        ) 
    def meta_data_extractor(self):
        return Agent(

        )
    
    


