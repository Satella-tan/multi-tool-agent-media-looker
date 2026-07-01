# Multi-Tool AI Agent

An autonomous conversational AI agent that selects and executes tools to evaluate math expressions, search the web, and scan/fuzzy-search your local media directories. Powered by LangChain, FastAPI, and Qwen-3 (via Groq).

---

## Features
* **Math Evaluator:** Safely parses and solves basic operations (+, -, *, /) using native float operations.
* **Web Search:** Queries DuckDuckGo for live info.
* **Media Looker:** Scans your selected folders (.env) and indexes local media directories into a lightweight, JSON cache (data/media_index.json) to eliminate filesystem scan latency and searches your books, manga, and anime files using `rapidfuzz` against the local JSON cache.

---

## How to Install & Configure:

1. **Clone & setup venv:**
   ```bash
   git clone https://github.com/yourusername/multi-tool-ai-agent.git
   cd multi-tool-ai-agent
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   Create a `.env` file at the root:
   ```ini
   GROQ_API_KEY=your_groq_api_key
   MEDIA_DIRS=C:\Users\Pc\Desktop\BOOKS,E:\ANDRES\Media
   ```

---

## How to Run:

### Terminal Mode (Interactive Loop)
```bash
python cli.py
```

### REST API Server (FastAPI)
```bash
uvicorn main:app --reload
```
Once running, check out the interactive Swagger API documentation at: `http://127.0.0.1:8000/docs`

---

## API Usage (Curl Example)

**Endpoint:** `POST /chat`
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Do I have angel next door?\", \"session_id\": \"my-session\"}"
```

**Response:**
```json
{
  "response": "You have \"The Angel Next Door Spoils Me Rotten\" in your library, with 5 matching files found...",
  "tools_used": ["lookup_media"],
  "session_id": "my-session"
}
```
