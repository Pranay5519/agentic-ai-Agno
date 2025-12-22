from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import time
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.team import Team

load_dotenv()  # loads GOOGLE_API_KEY

model = Gemini(
    id="gemini-2.5-flash"
)


# 1. News Search Agent
news_agent = Agent(
    id="news_agent",
    name="News Agent",
    model=model,
    role="Get the latest news headlines and give summary",
    instructions=["You are a news search agent",
                  "Search for the latest news for a particular destination and give a summarized view"],
    tools=[DuckDuckGoTools()]
)

# 2. Web Search Agent
web_search_agent = Agent(
    id="web_search_agent",
    name="Web Search Agent",
    model=model,
    role="Get information for places to visit at the destination",
    instructions=["You are a web search agent",
                  "your goal is to search for places of interest for a particular destination"],
    tools=[DuckDuckGoTools()]
)

# Team
travel_agent = Team(
    members = [news_agent, web_search_agent],
    model = model, # explicity pass custom model for the team , otherwise openAi model will be used
    
    name ="Travel Agent",
    id ="travel_agent",
    role = "you are a team leader and you deligate tasks to your team members to plan a trip",
    instructions=["You are an expert travel agent",
                  "you team members can get latest news and places of interest for a particular destination",
                  "your task is to present the output using proper headlines"],
    stream=True,
    markdown=True,
    debug_mode=False  # enable to see the team interactions 
)

travel_agent.cli_app(stream = True , markdown = True)
