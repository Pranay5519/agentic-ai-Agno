from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from agno.workflow import Step, Workflow, Router, StepInput
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools

load_dotenv()  # loads GOOGLE_API_KEY   

model  = Gemini(
    id="gemini-2.5-flash")

def is_tech_topic(step_input: StepInput) -> list[Step]:
    """Condition to check whether the input topic is technical or not"""
    
    tech_keywords = ["technology",
                     "tech",
                     "software",
                     "ai",
                     "artificial intelligence",
                     "machine learning", 
                     "computers",
                     "programming",
                     "hardware",
                     "internet",
                     "gadgets",
                     "electronics"]
    
    user_input = step_input.input or ""
    if user_input:
        user_input = user_input.lower()
        # check if any tech word in the input
        if any(keyword in user_input for keyword in tech_keywords):
            return [hackernews_search_step]
        else:
            return [duckduckgo_search_step]
        
        
# duckduckgo search agent
duckduckgo_search_agent = Agent(
    id="duckduckgo-agent",
    name="DuckDuckGo Search Agent",
    model=model,
    tools=[DuckDuckGoTools()],
    instructions=["You are an expert web search agent.",
                  "Provide accurate and relevant information based on user's queries"]
)

hackernews_agent = Agent(
    id="hackernews-agent",
    name="HackerNews Search Agent",
    model=model,
    tools=[HackerNewsTools()],
    instructions=["You are an expert agent",
                  "You retrieve relevant and latest news from hacker news platform"]
)

content_creation_agent = Agent(
    id="content-creation-agent",
    name="Content Creation Agent",
    model=model,
    instructions=["You are an expert in content creation and writing articles",
                  "You take in research data and create engaging, well structured articles",
                  "Format the content with proper headings, bullet points and clear conclusions"]
)

duckduckgo_search_step = Step(
    name="DuckDuckGo Search Step",
    agent=duckduckgo_search_agent,
    description="Performs web search using DuckDuckGo Search"
)

hackernews_search_step = Step(
    name="HackerNews Search Step",
    agent=hackernews_agent,
    description="This step Retrieves latest news and trending topics from Hacker news"
)

content_creation_step = Step(
    name="Content Creation Step",
    agent=content_creation_agent,
    description="Creates engaging articles based on the data provided"

)


# create the router step
router_step = Router(
    name="Topic Router Step",
    description="Routes the workflow based on whether the topic is tech based or not",
    choices=[duckduckgo_search_step, hackernews_search_step],
    selector=is_tech_topic
)

# create the workflow
workflow = Workflow(
    id="research-and-create-workflow",
    name="Research and Publish Article Workflow",
    steps=[router_step, content_creation_step],
    description="A workflow that researches a topic from different sources based on if the topic is tech related or not and writes an engaging article based on the research"
)

workflow.print_response(input="Create an article about latest events due to climate change",
                        stream=True, markdown=True)