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

def run_agent(prompt: str, history: list = None) -> dict:
    """
    Runs the agent with a given prompt and optional conversation history.
    Returns a dict containing:
    - 'response': The final text reply from the agent.
    - 'tools_used': A list of unique tool names called during the run.
    - 'messages': The updated list of all conversation messages.
    """
    messages = []
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    result = agent_graph.invoke({"messages": messages})

    # Extract any tools called during the model run
    tools_used = []
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tools_used.append(tc["name"])

    # Unique tools list
    tools_used = list(set(tools_used))
    response_text = result["messages"][-1].content

    return {
        "response": response_text,
        "tools_used": tools_used,
        "messages": result["messages"]
    }
