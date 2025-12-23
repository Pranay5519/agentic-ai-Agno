from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import time
from agno.workflow import Step, Workflow
load_dotenv()  # loads GOOGLE_API_KEY

model = Gemini(
    id="gemini-2.5-flash")

#essay writing agent 

essay_writing_agent = Agent(
    id="essay_writing_agent",
    model = model,
    name = "Essay Writing Agent",
    instructions=["You are an expert in writing essays",
                  "Write well structured essays on a variety of topics",
                  "Limit your response to a maximum of 500 words"])

# extraction agent to extract imp points from the essay
extraction_agent = Agent(
    id="extraction-agent",
    name="Extraction Agent",
    instructions=["You are an expert at extracting important points from the generated essay",
                  "Summarize the key points in a concise manner",
                  "Your output should be in a good format"],
    model=model,
    markdown=True
)

# ================STEPS===================

essay_writing_step = Step(
    name = "essay writing step",
    agent = essay_writing_agent,
    description="Generates an essay based on the user's topic"
)
extraction_step = Step(
    name="Information Extraction Step",
    agent=extraction_agent,
    description="Extracts important points from the essay generated in the previous step"
)

workflow = Workflow(
    id = "essay_workflow",
    name = "Essay Writing Workflow",
    steps = [essay_writing_step , extraction_step],
   description="A workflow that first writes an essay on a given topic and then extracts important points from that essay"

)

# execute the workflow

workflow.print_response(input = "The topic is about the impact of technology on education" ,stream=  True  , markdown = True)
