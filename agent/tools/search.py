from langchain_core.tools import tool
from duckduckgo_search import DDGS

@tool
def ddg_search(query: str) -> str:
    """
    Search the web for the given query using DuckDuckGo.
    Returns the top 3 search results formatted as plain text.
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            if not results:
                return f"No search results found for query: '{query}'"
            
            formatted_results = []
            for i, r in enumerate(results, 1):
                title = r.get("title", "No Title")
                url = r.get("href", "No URL")
                snippet = r.get("body", "No Snippet")
                formatted_results.append(
                    f"Result {i}:\n"
                    f"Title: {title}\n"
                    f"URL: {url}\n"
                    f"Snippet: {snippet}\n"
                )
            return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error performing web search: {str(e)}"
