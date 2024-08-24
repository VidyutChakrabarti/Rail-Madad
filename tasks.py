from crewai import Task 

class Main_Tasks:
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
            tools=[],
            agent=agent,
        )

    def categorize_into_departments(self, agent, context):
        return Task(
            description=(
                "Classify the complaint into the most appropriate department based on the summarized issues:\nIssues: {issues}\nDepartments: {departments}\n"
                "Using the context provided, which summarizes the main issues from the complaint, determine the single department that is best equipped to handle the issues."
            ),
            expected_output=(
                "Return only one department name that is the best fit to address the complaint.\n"
                "Example Output: {'department': 'Finance'}"
            ),
            async_execution=True, 
            agent=agent,
            context=context
        )
    
    def schedule(self, agent, context): 
        return Task(
            description=(
                "Evaluate the urgency of the issues summarized in this list: {issues}."
                "Assign a priority rating from 1 to 5, with 1 being the least urgent and 5 being the most urgent.\n"
                "Base your rating on the severity of the issues within the department it has been assigned to and the relevant scheduling schema provided.\nPre-categorized topics:\n{scheduling_schema}\n"
                "If an issue does not match a pre-categorized subset or if the complaint specifies reasons for higher urgency, assign a rating based on {urgency_eval}.\n"
                "Complaint: {complaint}\n"
            ), 
            expected_output=(
                "A single integer from 1 to 5 indicating the urgency level of the complaint.\n"
                "Example Output: {'Priority level': 1}"
            ), 
            async_execution=True, 
            agent=agent, 
            context=context
        ) #the department must be passed a context. 

class Sub_tasks: 
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
        """Example output
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


