from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from agno.db.json import JsonDb
load_dotenv()  # loads GOOGLE_API_KEY

model = Gemini(
    id="gemini-2.5-flash"
)

#session id 
session_id = "session_1"

#create a database
db = JsonDb(db_path = "chat_history_db", 
            session_table = "session_history")

agent = Agent(
    model=model,
    name="agent_with_memory",
    markdown=True,
    stream = True,
    add_history_to_context = True,
    session_id = session_id , 
    num_history_runs  =3,
    db = db
)

agent.print_response(input = "My name is Pranay")
agent.print_response(input = "What is my name?")
# agent.print_response(input = "Explain the theory of relativity in simple terms only single line",stream = True)   
# agent.print_response(input = "Tell me what topic am i talking about",stream = True)
# agent.print_response(input = "Where do I live?",stream = True)
# agent.print_response(input = "Who am I?",stream = True)

messages = agent.get_chat_history(session_id)
for msg in messages:
    role , content = msg.role , msg.content
    if role == "system":
        continue
    else:
        print(f"Role: {role} , Message :{content} ")