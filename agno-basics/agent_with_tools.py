from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.db.sqlite import SqliteDb
load_dotenv()  # loads GOOGLE_API_KEY

model = Gemini(
    id="gemini-2.5-flash")

# session id
session_id = "session_1"
# create a database
#db = SqliteDb(db_path="chat_history_db.sqlite")

# web search tool
web_search = DuckDuckGoTools()

agent = Agent(
    model= model , 
    tools = [web_search],
    instructions = "You are an AI assistant that helps users find information using web search.",
    stream = True,
    #db = db,
    markdown = True)

agent.print_response("What is Trending On earth Today?")
