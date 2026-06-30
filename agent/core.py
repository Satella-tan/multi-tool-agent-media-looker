import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from agent.tools.calculator import calculate
from agent.tools.search import ddg_search

# Load environment variables from .env at the root
load_dotenv()

# Initialize the LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.0
)

# Define tools
tools = [calculate, ddg_search]

# System prompt for the agent
SYSTEM_PROMPT = """You are a helpful and intelligent AI assistant.
You have access to a set of tools to help you answer questions.
Always use the appropriate tool when needed to ensure accuracy, especially for calculations.
If you use a tool, explain your reasoning and present the tool's result clearly.
"""

agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

def run_agent(prompt: str) -> str:
    """
    Runs the agent with a given prompt and returns the final response string.
    """
    inputs = {"messages": [{"role": "user", "content": prompt}]}
    result = agent_graph.invoke(inputs)
    return result["messages"][-1].content
