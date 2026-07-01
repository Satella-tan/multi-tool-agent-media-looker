# Multi-Tool AI Agent

An autonomous conversational AI agent that selects and executes tools to evaluate math expressions, search the web, and scan/fuzzy-search your local media directories. Powered by LangChain, FastAPI, and Qwen-3 (via Groq).

---

## Features
* **Math Evaluator:** Safely parses and solves basic operations (+, -, *, /) using native float operations.
* **Web Search:** Queries DuckDuckGo for live info.
* **Media Looker:** Normalizes filenames (strips group tags like `[Sokudo]`, qualities like `1080p`, etc.) and fuzzy-searches your books, manga, and anime files using `rapidfuzz` against a local JSON cache.

---

## How to Install & Configure:

<<<<<<< HEAD
1. **Clone & setup venv:**
=======
The media library tool is the unique component of the project. It allows you to search files stored locally on your machine using natural language (e.g., *"Do I have any studio ghibli movies?"* or *"Do I have 1984 by Orwell?"*) without doing slow, redundant filesystem scans every time.

### How It Works:
* **JSON Caching:** On its first run (or when requested), it recursively scans your configured folders and writes a fast lookup cache to `data/media_index.json`. This index is automatically ignored by Git to protect your privacy and local paths.
* **Smart Filename Normalization:** Anime and media files often contain noisy tags (fansub groups like `[Sokudo]`, parentheses, quality/codec markers like `1080p BD AV1 x265`, and season/episode numbers like `S01E03`). The tool's normalization engine strips this noise out, transforming `[Sokudo] Amagi Brilliant Park - S00E01 [1080p BD AV1].mkv` into the clean query-friendly token `amagi brilliant park`.
* **Fuzzy Match Engine:** Queries are normalized and compared against the index using `rapidfuzz`. This finds the closest match even if you make typos or search with incomplete titles.
* **Supported Formats:**
  * **Books / Manga:** `.pdf`, `.epub`, `.mobi`, `.cbz`
  * **Videos / Anime:** `.mp4`, `.mkv`, `.avi`

---

## Setup & First-Time Installation

Follow these steps to set up and run the project on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Satella-tan/multi-tool-agent-media-looker.git
cd multi-tool-ai-agent
```

### 2. Set Up a Virtual Environment
Create and activate a Python virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: If you don't have a `requirements.txt` yet, install core dependencies: `pip install langchain langchain-groq python-dotenv duckduckgo-search rapidfuzz`)*

### 4. Configure Environment Variables (`.env`)
The agent requires a `.env` file at the root directory to store your Groq API key and local media paths.

1. Copy the example environment template:
>>>>>>> ae85a73b294be039ad8f8f70321136c889090a9e
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
