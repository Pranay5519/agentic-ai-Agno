from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from knowledge_base import knowledge_base
load_dotenv()  # loads GOOGLE_API_KEY
import time
from textwrap import dedent
model = Gemini(
    id="gemini-2.5-flash"
)


agent = Agent(
    model=model,
    knowledge=knowledge_base,
    name="Knowledge_Agent",
    search_knowledge=True,
    instructions=["you are a helpful assistant", "Answer as short as possible" , 
                  "whenever asked about Tubetalk.ai project, use the knowledge base to get the context",
                  "try not to hallucinate while responding",
                  "if you don't know the answer to a particular query just say I dont know"],
    stream=True,
    markdown=True
)
# agent.print_response("Hi how are you?")
# time.sleep(10)
# agent.print_response("Can You Tell me what is TubeTalk.ai Project and what is the progess of that project?")

agent.print_response("Tell me the name of the projectees of TubeTalk.ai project?")