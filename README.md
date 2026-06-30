# Multi-Tool AI Agent

A conversational AI assistant built in Python that autonomously decides which tools to call based on user input. It uses Groq's high-speed API (powered by **Qwen 3 32B**) and LangChain/LangGraph for orchestration. 

It is designed to run in your terminal (and easily extendable to a REST API) to help you perform mathematical calculations, search the web, and manage/query your local media library.

---

## Key Features & Tools

1. **Smart Calculator (`calculate`):** Safely parses and evaluates basic arithmetic operations (`+`, `-`, `*`, `/`) without using unsafe `eval()` functions.
2. **Web Search (`ddg_search`):** Fetches the top 3 search results from DuckDuckGo for general knowledge, news, and real-time updates.
3. **Local Media Search (`lookup_media`):** Fuzzy-searches your local media files (books, manga, anime, and shows).
4. **Media Index Update (`rebuild_index`):** Rescans your directories to update the local cache when files change.

---

## Deep Dive: Media Library Lookup (`media_looker.py`)

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
   ```bash
   cp .env.example .env
   ```
2. Open the newly created `.env` file and configure it:
   * **`GROQ_API_KEY`**: Obtain a free API key at [console.groq.com](https://console.groq.com/) and paste it here.
   * **`MEDIA_DIRS`**: Provide a comma-separated list of absolute paths to the folders you want the agent to search.
   
   Example `.env` configuration:
   ```ini
   GROQ_API_KEY=gsk_your_actual_key_here
   MEDIA_DIRS=C:\Users\Pc\Desktop\BOOKS,E:\ANDRES\Media
   ```

### 5. Running the Agent
Start the terminal test harness:
```bash
python main.py
```

---

## Example Prompts to Try

* **Math:** `What is 340 * 1.16?` (Triggers `calculate`)
* **Web Search:** `who won the last world cup?` (Triggers `ddg_search`)
* **Local Media:** `Do I have 1984 by Orwell?` or `Do I have Amagi Brilliant Park?` (Triggers `lookup_media` using your local index)
* **Update Library:** `Update my media library` (Triggers `rebuild_index` to rescan folders and overwrite the JSON cache)
* **Multi-Step Chain:** `Search who won the last World Cup and calculate how many years ago that was` (Triggers search, then uses the calculator on the retrieved year)
