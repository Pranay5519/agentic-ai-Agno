from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
load_dotenv()  # loads GOOGLE_API_KEY
import time
from textwrap import dedent
model = Gemini(
    id="gemini-2.5-flash"
)

db  = SqliteDb(db_file="chat_history_db/chat_history.db")

web_search = DuckDuckGoTools()

def add_key_point(session_state: dict, point: str) -> str:
    """tool to add key points to the session state"""
    # fetch the list
    points_list = session_state["key_points"]
    # add point to the points list
    points_list.append(point)
    
    return f"Point: {point} added to the session state"
    

# build the agent
agent = Agent(
    name="my_agent",
    model=model,
    db=db,
    session_id="session_2",
    user_id="user1",
    session_state={"key_points": []},
    tools=[add_key_point, web_search],
    instructions=dedent("""
                you are an expert assistant. your task is to:
                1. Create summary on the topic and stick to the word count if provided.
                2. You have the capability to access the web using web search tool. try to generate summary with the latest information.
                3. You have access to a tool called as 'add_key_point' which adds a key_point from the summary to the session state.
                4. Add key point only when asked for.
                5. The summary created should include both advantages and disadvantages.
                """),
    add_history_to_context=True,
    num_history_runs=5,
    add_session_state_to_context=True,
    markdown=True,
    stream=True,
)

agent.print_response("Write a 50 word summary on the topic: 'AI Agents and its future'. Use the latest information to generate the response.")
time.sleep(20)
agent.print_response("add key points from the summary generated above. The number of points depends on the summary")


#agent.print_response("What topic are we talking about?")
time.sleep(10)
agent.print_response("List down the key points from the recent summary generated for me in proper format")

print(agent.get_session_state("session_2"))