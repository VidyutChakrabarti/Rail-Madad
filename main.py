from agents import Main_agents, Helper_agents, ChatAgents
from tasks import Main_Tasks, Sub_tasks
from PIL import Image
from crewai import Crew, Process

main_agents = Main_agents()
main_tasks = Main_Tasks()
chat_agent = ChatAgents()
sub_agents = Helper_agents()
sub_tasks = Sub_tasks() 

#initializing agents 
complaint_analyzer = main_agents.complaint_analysis_agent()
department_router = main_agents.department_routing_agent()
scheduler = main_agents.scheduler()
writer = main_agents.support_agent()
editor = main_agents.support_quality_assurance_agent()
chatter = chat_agent.chatagent()
#searcher = chat_agent.Searchagent()
# image_describer = sub_agents.image_analysis_agent()
# metadata_extractor = sub_agents.meta_data_extractor()
# video_analyzer = sub_agents.video_analyser()

#initializing tasks
complaintAnalysis = main_tasks.extract_main_issues(complaint_analyzer)
routing = main_tasks.categorize_into_departments(department_router, [complaintAnalysis])
scheduling = main_tasks.schedule(scheduler, [complaintAnalysis, routing])
respond = main_tasks.write_response(writer, [complaintAnalysis, routing, scheduling])
proof_read = main_tasks.proof_read(editor, [respond])
livechat = main_tasks.chatting(chatter)
#searching = sub_tasks.search_internet(searcher)

crew = Crew(
                agents = [complaint_analyzer, department_router, scheduler, writer, editor], 
                tasks = [complaintAnalysis, routing, scheduling, respond, proof_read], 
            )
chatcrew = Crew(
    agents=[chatter], 
    tasks = [livechat],
    memory=True,
    embedder={
                "provider": "google",
                "config":{
                "model": 'models/embedding-001',
                "task_type": "RETRIEVAL_DOCUMENT",
                "title": "Embeddings for Embedchain"
            }
        }
)
