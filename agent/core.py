import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from agent.tools.calculator import calculate
from agent.tools.search import ddg_search
from agent.tools.media_looker import lookup_media, rebuild_index

# Load environment variables from .env at the root
load_dotenv()

# Use your preferred LLM, recommend qwen/qwen3-32b bc it returns JSON
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0.0
)

# Define tools
tools = [calculate, ddg_search, lookup_media, rebuild_index]

# System prompt for the agent
SYSTEM_PROMPT = """You are a helpful and intelligent AI assistant.
You have access to the following tools:
- Use 'calculate' for any mathematical calculations or evaluations.
- Use 'ddg_search' to search the web for external information, general knowledge, or news.
- Use 'lookup_media' to search the user's local media library for books, manga, anime, and video files.
- Use 'rebuild_index' to rescan and update the local media library cache.

When a user asks if they have a book, anime, manga, movie, or series (e.g. 'Do I have ...'), always use the 'lookup_media' tool to check their local library.
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
