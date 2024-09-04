from crewai import Task 

class Main_Tasks():
    def extract_main_issues(self, agent):
        return Task(
            description=(
                "Analyze the following complaint and identify all distinct issues:\n{complaint}\n"
                "Each issue should be grouped under a relevant subject heading. Provide a concise summary for each identified subject."
            ),
            expected_output=(
                "A list of summarized subjects covering all issues from the complaint is expected.\n"
                "Each subject should be a short, descriptive phrase that encapsulates the core of the issue it represents.\n"
                "Example Output: ['coach cleanliness', 'dysfunctional washrooms', 'staff behavior']"
            ),
            agent=agent,
        )

    def categorize_into_departments(self, agent, context):
        return Task(
            description=(
                "Classify the complaint into the most appropriate department based on the summarized issues in the context provided.\nDepartments: {departments}\n"
                "Using the context provided, which summarizes the main issues from the complaint, determine the single department that is best equipped to handle the issues."
            ),
            expected_output=(
                "Return only one department name that is the best fit to address the complaint and its description provided in Departments dictionary.\n"
                "Example Output: ['department': 'Finance', 'handling':'Responsible for budgeting, accounting, and financial management.']"
            ),
            agent=agent,
            context=context
        )
    
    def schedule(self, agent, context): 
        return Task(
            description=(
                "Evaluate the urgency of the issues summarized in the list provided in context."
                "Assign a single priority rating from 1 to 5 taking into account all the issues, with 1 being the least urgent and 5 being the most urgent.\n"
                "Base your rating on the severity of the issues within the department it has been assigned to."
                "If an issue does not match a pre-categorized subset or if the complaint specifies reasons for higher urgency, you must re-evaulate."
                "Complaint: {complaint}\n"
            ), 
            expected_output=(
                "A single integer from 1 to 5 indicating the urgency level of the complaint.\n"
                "Example Output: ['Priority': 1]"
            ), 
            async_execution=False, 
            agent=agent, 
            context=context
        )
    def write_response(self, agent, context): 
       return Task(
        description = (
            "A customer has a complaint:\n"
            "{complaint}\n\n"
            "Make sure to use everything you know "
            "to provide the best support possible."
            "You must strive to provide a complete "
            "and accurate response addressing every issue listed in the context."
            " Elaborate on how your department is working/plans to work on all the individual issues and"
            " generate a supportive complete response."
          ),
          expected_output= (
            "The response must address all the issues identified and provide an estimated time of hearing back. "
            "It must be written in formal tone and reassure customers of quick actions in a very friendly way.\n"
            """Example output: 
            Dear Sir/Madam,\n
            Thank you for bringing these issues to our attention. We sincerely apologize for the inconvenience you experienced during your journey. Your feedback is crucial in helping us improve our services.
            Coach Cleanliness & Washroom Conditions: We are addressing the cleanliness issues with immediate effect. Our cleaning staff will undergo additional training, and we will increase the frequency of cleaning checks. We aim to resolve this within the next two weeks.
            AC Malfunction: Our technical team is investigating the air conditioning issues. We are prioritizing this and expect to have a solution within a week.
            Staff Conduct: We are conducting a thorough review of staff behavior and will provide additional training to ensure professionalism and courtesy. This will be addressed within the next two weeks.
            Food Service Quality: We are working with our catering partners to improve the quality and temperature of the meals served. Changes will be implemented within the next week.
            Train Delay: We are reviewing our communication protocols to ensure timely updates are provided to passengers. This will be improved within the next week.
            You can expect a detailed response from us within two weeks. We appreciate your patience and understanding as we work to enhance your travel experience.\n
            Warm regards, Rail-Madad AI-Assitant, Public relations Department, Indian Railways.
            """
          ),
        async_execution=True, 
        agent=agent, 
        context=context
       )
    def proof_read(self, agent, context):
       return Task(
          description=(
            "Review the response drafted by the Senior Support Representative for the complaint:\n{complaint}\n"
            "Ensure that the answer is comprehensive, accurate, and adheres to the "
            "high-quality standards expected for customer support.\n"
            "Verify that all parts of the customer's inquiry have been addressed "
            "thoroughly, with a helpful and friendly tone. You must also ensure the subject summarizes "
            "the response well within one sentence. "
            "Ensure the response is well-supported and "
            "leaves no questions unanswered."
          ), 
          expected_output=(
        "A final, detailed, and informative response "
        "ready to be mailed to the customer.\n"
        "This response should fully address the "
        "customer's issues within 250 words strictly, incorporating all "
        "relevant feedback and improvements. "
        "Ensure that the final answer is written like a formal letter from a prestigious brand (Indian Railways)."
        """Example output: 
        Dear Sir/Madam,
        Date: 12/08/2004,
        Subject: Response to the complaint lodged regarding your journey on train number 99783 dated dd/mm/yyyy. 
        We sincerely apologize for the inconvenience you experienced during your recent journey with Indian Railways. Your feedback is invaluable, and we are committed to addressing the issues promptly.
        Coach Cleanliness & Washroom Conditions: We are enhancing our cleaning protocols and training staff to ensure better cleanliness within two weeks.
        AC Malfunction: Our technical team is prioritizing the air conditioning issues and expects a solution within a week.
        Staff Conduct: We are reviewing staff behavior and providing additional training to ensure professionalism and courtesy within two weeks.
        Food Service Quality: We are working with our catering partners to improve meal quality and temperature within a week.
        Train Delay: We are improving our communication protocols to provide timely updates to passengers within a week.
        You can expect a detailed response from us within two weeks. We appreciate your patience and understanding as we work to enhance your travel experience.
        Yours sincerely,

        Rail-Madad AI-Assistant, 
        Commercial Department,
        Indian Railways."""
        ), 
        async_execution=False, 
        agent=agent, 
        context=context
       )
    def chatting(self, agent):
       return Task(
        description = ("A user is chatting with you. "
        "You are a professional supporting agent who gives reposnses taking into account the historical context of the chat "
        "and also keeping your responses to the point and brief, optimize and plan the use of tools to make minimum calls before execution.\nPrompt: {prompt}\n 'historical context': {history}"              
        ), 
        expected_output = ("Short to the point answers are needed. But you must also provide complete and professional responses that answer all queries within the prompt taking into account the history."
        """Example output:
        Rajdhani Express Reviews:
        Overall Rating: Generally positive, with a rating of 4.3/5 based on 2668 reviews1.
        Pros: Punctuality, cleanliness, and service are often praised1.
        Cons: Some passengers have reported issues with food quality and cleanliness in certain coaches1.
        Ticket Price from Nagpur to Bangalore:
        Rajdhani Express (22692): Approximately ₹2896 for 3A, ₹1860 for 3A (Tatkal), ₹2600 for 2A, and ₹1480 for Sleeper (Tatkal).
        Is there anything else you need help with? """), 
        agent=agent,
        async_execution=False 
       )
    
class Sub_tasks(): 
   def image_analysis_task(self, agent, image_path):
    return Task(
        name='Image Analysis',
        description="""Analyze the image and generate a detailed description, focusing on any potential complaints that may be derived from the image.
        Include any textual information extracted using OCR, if present.\n
        Steps:
        1. Load the image from the specified path.
        2. Evaluate the visual content of the image.
        3. Use OCR to extract any textual information present in the image.
        4. Generate a comprehensive description of the image, emphasizing potential complaints.
        5. Include a summary of extracted text, if present.
        6. Return the detailed description.
        """,
        expected_output = (
        "provide a description of the image within 100 words. Also include a list of potential complaints that may be derived from the image relating to railways."
        """Example output:
        Image Description: The image shows the interior of a railway coach that is visibly dirty and poorly maintained. 
        The floor is covered with litter, including empty water bottles, food wrappers, and newspapers. 
        The seats appear to be stained and there are visible marks on the walls. The windows are smudged, and there is a general sense of neglect and lack of cleanliness.\n
        Potential Complaints:
            The overall cleanliness of the railway coach is severely lacking.
            The presence of litter on the floor indicates inadequate cleaning services.
            Stained seats and marked walls suggest poor maintenance and hygiene standards.
            Smudged windows reduce visibility and contribute to an unpleasant travel experience.
"""),
        image_path=image_path,
        agent=agent
    )
   



