from agno.workflow import Step, Workflow, Parallel
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.hackernews import HackerNewsTools
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini

load_dotenv()

model = Gemini(
    id="gemini-2.5-flash"
)

# wikipedia search agent
wikipedia_agent = Agent(
    id="wikipedia-agent",
    name="Wikipedia Search Agent",
    instructions=[
        "You are an expert knowledge retrieval agent using Wikipedia",
        "Provide accurate, factual, and concise information",
        "Add heading: Source: Wikipedia"
    ],
    model=model,
    tools=[WikipediaTools()],
)

# duckduckgo agent
duckduckgo_agent = Agent(
    id="duckduckgo-agent",
    name="DuckDuckGo Search Agent",
    instructions=[
        "You are an expert web search agent using DuckDuckGo",
        "Provide accurate and relevant information",
        "Add heading: Source: DuckDuckGo Search"
    ],
    model=model,
    tools=[DuckDuckGoTools()],
)

# hackernews agent
hackernews_agent = Agent(
    id="hackernews-agent",
    name="HackerNews Agent",
    instructions=[
        "You are an expert in retrieving trending topics and latest news from Hacker News",
        "Add heading: Source: HackerNews"
    ],
    model=model,
    tools=[HackerNewsTools()],
)

# report generation agent
report_generation_agent = Agent(
    id="report-generation-agent",
    name="Report Generation Agent",
    model=model,
    instructions=[
        "You are an expert in report generation",
        "Compile information from Wikipedia and DuckDuckGo",
        "Mention sources clearly",
        "Output must be well-structured"
    ],
    markdown=True
)

# ================= STEPS =================

wikipedia_search_step = Step(
    name="Wikipedia Search Step",
    agent=wikipedia_agent,
    description="Retrieves factual information from Wikipedia"
)

duckduckgo_search_step = Step(
    name="DuckDuckGo Search Step",
    agent=duckduckgo_agent,
    description="Performs web search using DuckDuckGo"
)

hackernews_search_step = Step(
    name="HackerNews Search Step",
    agent=hackernews_agent,
    description="Retrieves trending topics from HackerNews"
)

report_generation_step = Step(
    name="Report Generation Step",
    agent=report_generation_agent,
    description="Generates a report from collected information"
)

# parallel step
parallel_steps = Parallel(
    wikipedia_search_step,
    duckduckgo_search_step,
    #hackernews_search_step,
    name="Parallel Search Step",
    description="Parallel search using Wikipedia, DuckDuckGo, and HackerNews"
)

parallel_workflow = Workflow(
    id="parallel_search_workflow",
    name="Parallel Search Workflow",
    steps=[parallel_steps, report_generation_step],
    description="Parallel knowledge retrieval and report generation workflow"
)

parallel_workflow.print_response(
    input="topic: AI",
    stream=True,
    markdown=True
)
