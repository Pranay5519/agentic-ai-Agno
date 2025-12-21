from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
load_dotenv()  # loads GOOGLE_API_KEY

model = Gemini(
    id="gemini-2.5-flash"
)

#session id 
user_id = "user1"

#create a database
db = SqliteDb(db_file="demo.db")
agent = Agent(
    model=model,
    name="agent_with_memory",
    markdown=True,
    stream = True,
    add_history_to_context = True, 
    num_history_runs  =5,
    db = db
)
# conversation 1 session id  -> session_id  = session transformers
# conversation 2 session id  -> session_id  = session gpt

# create sessions 
session_transformers = "session_transformers"
session_gpt = "session_gpt"

#sesison Transformers
agent.print_response(input = "what are transformers? answer in single line" ,session_id = session_transformers)
agent.print_response(input = "what topic am I taling about?", session_id = session_transformers)

#session GPT
agent.print_response(input = "what is gpt model? answer in single line", session_id = session_gpt)
agent.print_response(input = "what topic am I taling about?", session_id = session_gpt)

print() 
print()

print("============ Tranformer Messages =================")
messages_1 = agent.get_chat_history(session_transformers)

for message in messages_1:
    role, content = message.role, message.content
    if role == "system":
        continue
    else:
        print(f"Role: {role}, Message: \n{content}")
        
print("\n\n============ GPT Messages =================")
messages_2 = agent.get_chat_history(session_gpt)

for message in messages_2:
    role, content = message.role, message.content
    if role == "system":
        continue
    else:
        print(f"Role: {role}, Message: \n{content}")