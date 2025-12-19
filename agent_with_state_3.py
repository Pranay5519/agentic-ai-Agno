from agno.agent import Agent
from agno.models.google  import Gemini
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb 
import time

load_dotenv()  # loads GOOGLE_API_KEY
model = Gemini(
    id="gemini-2.5-flash")

# db

db = SqliteDb(db_file="session_state_db/shopping.db")

session_id = "1"
user_id = "pranay"

# define a tool that adds items to shopping list in session state

def add_item(session_state: dict, item: str) -> str:
    """Add an item to the shopping list"""
    # lowercase the item
    item = item.lower()
    # fetch the shopping list
    shopping_list = session_state["shopping_list"]
    
    # check if item in list or not
    if item in shopping_list:
        return f"{item} already in shopping list"
    else:
        shopping_list.append(item)
        return f"{item} added to the shopping list"

# define tool to remove item from shopping list
def remove_item(session_state: dict, item: str) -> str:
    """Removes an item from the shopping list for the items i have already purchased"""
    # lowercase the item
    item = item.lower()
    # fetch the shopping list
    shopping_list = session_state["shopping_list"]
    
    # check item in list or not
    if item not in shopping_list:
        f"{item} not in shopping list. Add the item first"
    else:
       # remove the item from shopping list
       shopping_list.remove(item)
       return f"{item} removed from shopping list"
  
def clear_list(session_state: dict) -> str:
    """Clears the shopping list of all items and gives you empty list"""
    shopping_list = session_state["shopping_list"]
    shopping_list.clear()
    return "Cleared the shopping list of all items" 

def list_items(session_state: dict) -> str:
    """List down all the items in shopping list"""
    # check whether shopping list is empty or not
    # fetch the shopping list
    shopping_list = session_state["shopping_list"]
    
    if shopping_list:
        list_of_items = "\n".join([f"- {item}" for item in shopping_list]) ## - Apple - Banana
        return f"The shopping list is: {list_of_items}"
    else:
        return "The shopping list is empty"
    
       
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
    tools={add_item , remove_item , clear_list} # if you dont use tool parameter and update the shopping list the items
                     # will not be stored in session_state but only in context i.e temporary
)

agent.print_response("Can you tell me what is on the shopping list")
print(f"The session state is: {agent.get_session_state(session_id)}")
time.sleep(5)

agent.print_response("Add milk to the shopping list")
print(f"The session state is: {agent.get_session_state(session_id)}")
time.sleep(5)

agent.print_response("Add eggs and bread to my shopping list")
print(f"The session state is: {agent.get_session_state(session_id)}")
time.sleep(5)

agent.print_response("I have bought milk and eggs")
print(f"The session state is: {agent.get_session_state(session_id)}")
time.sleep(5)

agent.print_response("what is on my list?")
print(f"The session state is: {agent.get_session_state(session_id)}")
time.sleep(5)

agent.print_response("Clear everything from the shopping list and add butter and curd to the list")
print(f"The session state is: {agent.get_session_state(session_id)}")
time.sleep(5)

agent.print_response("Remove oranges from the shopping list")
print(f"The session state is: {agent.get_session_state(session_id)}")