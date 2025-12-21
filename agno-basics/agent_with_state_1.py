from agno.agent import Agent
from agno.models.google  import Gemini
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb 

load_dotenv()  # loads GOOGLE_API_KEY
model = Gemini(
    id="gemini-2.5-flash")

# db

db = SqliteDb(db_file="session_state_db/temp.db")
session_id = "state_session_1"
user_id = "user_1"
user_info = {"name": "pranay", "age": 30}
agent = Agent(
    model=model,
    name="agent_with_session_state",
    markdown=True,
    stream=True,
    add_session_state_to_context=True,
    num_history_runs=5,
    db=db,
    session_id=session_id,
    user_id=user_id,
    session_state=user_info
)

#agent.print_response(input="Can you tell me my name and age",session_state = {"name": "pranay", "age": 30})

print(agent.get_session_state())