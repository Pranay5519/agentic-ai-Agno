from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv

load_dotenv()  # loads GOOGLE_API_KEY

model = Gemini(
    id="gemini-2.5-flash"
)

agent = Agent(
    model=model,
    name="agent1",
    markdown=True,
    stream = True
)

agent.print_response("Explain the theory of relativity in simple terms only 100 words",stream = True)

agent.print_response("Tell me what topic am i talking about",stream = True)