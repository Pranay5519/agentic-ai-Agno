from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
load_dotenv()  # loads GOOGLE_API_KEY
from textwrap import dedent
model = Gemini(
    id="gemini-2.5-flash"
)

db  = SqliteDb(db_file="chat_history_db/chat_history.db")

def add_keypoints(session_state: dict, point: str) -> str:
    "add key points to session state"
    points_list = session_state["key_points"]
    points_list.append(point)
    return f"{point} added. Key points updated: {points_list}"

agent = Agent(
    model=model,
    name="agent1",
    markdown=True,
    stream = True,
    db = db,
    session_id = "chat_session_1",
    user_id = "user_1",
    add_history_to_context = True,
    add_session_state_to_context =True,
    num_history_runs = 5,
    session_state = {"key_points": []},
    tools = {add_keypoints},
    instructions = dedent("""You are an expert tutor 
                          1.) Create summary on the topic and stick to word count
                          2) you have access to tool called as add_keypoints which helps you add key points to session state.
                          Use this tool to add key points whenever you find something important in the topic being discussed. 
                          The session state has a key called key_points which is a list of all the key points added so far.""")
)

agent.print_response("Explain what is Crew AI only in 100 words",stream = True)

agent.print_response("Tell me what topic am i talking about",stream = True)

print(agent.get_session_state(session_id="chat_session_1"))