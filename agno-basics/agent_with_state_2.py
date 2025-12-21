from agno.agent import Agent
from agno.models.google  import Gemini
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb 

load_dotenv()  # loads GOOGLE_API_KEY
model = Gemini(
    id="gemini-2.5-flash")

# db

db = SqliteDb(db_file="session_state_db/temp.db")

session_id = "1"
user_id = "user_2"

# define a tool that adds items to shopping list in session state
def add_item(session_state : dict , item :str) -> str:
    """Adds an item to the shopping list in session state."""
    
    shopping_list = session_state["shopping_list"]
    shopping_list.append(item)
    return "The shopping list has been updated : {}".format(shopping_list)
agent = Agent(
    model=model,
    name="agent_with_session_state",
    markdown=True,
    stream=True,
    add_session_state_to_context=True,
    num_history_runs=5,
    db=db,
    session_state={"shopping_list": ["eggs", "milk", "bread"]},
    instructions="You are an expert in maintaining shopping lists. You have access to shopping list: {shopping_list}",
    session_id=session_id,
    user_id=user_id , 
    tools={add_item} # if you dont use tool parameter and update the shopping list the items
                     # will not be stored in session_state but only in context i.e temporary
)

agent.print_response(input="Add apples and tomatoes to my shopping list")

print("The session state is ",agent.get_session_state(session_id))