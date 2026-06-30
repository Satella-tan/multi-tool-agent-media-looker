import os
import re
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.tools import tool
from rapidfuzz import process, fuzz

load_dotenv()

SUPPORTED_EXTENSIONS = {
    ".pdf", ".epub", ".azw3", ".mobi", ".cbz", ".cbr", ".mp4", ".mkv", ".avi", ".mov",
}

INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "media_index.json")
INDEX_PATH = os.path.normpath(INDEX_PATH)


def _get_media_dirs():
    """Read MEDIA_DIRS from .env and return as a list of paths."""
    dirs_str = os.getenv("MEDIA_DIRS", "")
    if not dirs_str:
        return []
    return [d.strip() for d in dirs_str.split(",") if d.strip()]


def _normalize(filename):
    """
    Normalize a filename for fuzzy matching.
    Strips extension, fansub tags [like this], codec/resolution info,
    season/episode markers, then lowercases and collapses whitespace.
    """
    name = os.path.splitext(filename)[0]           # remove extension
    name = re.sub(r"\[.*?\]", "", name)             # remove [fansub tags]
    name = re.sub(r"\(.*?\)", "", name)             # remove (parenthesized info)
    name = re.sub(r"S\d{1,2}E\d{1,2}", "", name, flags=re.IGNORECASE)  # remove S01E02
    name = re.sub(r"Season\s*\d+", "", name, flags=re.IGNORECASE)       # remove Season 01
    name = re.sub(r"\b(1080p|720p|480p|BD|AV1|HEVC|x264|x265|dual\s*audio|v\d)\b", "", name, flags=re.IGNORECASE)
    name = re.sub(r"[^a-zA-Z0-9\s]", " ", name)    # punctuation to spaces
    name = re.sub(r"\s+", " ", name).strip().lower()
    return name


def _build_index(media_dirs):
    """
    Recursively scan media_dirs, build the index, and write it to disk.
    Returns a summary string.
    """
    entries = []
    for base_dir in media_dirs:
        if not os.path.isdir(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            for filename in files:
                ext = os.path.splitext(filename)[1].lower()
                if ext not in SUPPORTED_EXTENSIONS:
                    continue
                full_path = os.path.join(root, filename)
                folder = os.path.basename(root)
                entries.append({
                    "filename": filename,
                    "normalized": _normalize(filename),
                    "extension": ext,
                    "folder": folder,
                    "full_path": full_path,
                })

    index_data = {
        "indexed_at": datetime.now().isoformat(),
        "total_files": len(entries),
        "entries": entries,
    }

    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

    folder_count = len(media_dirs)
    return f"Index rebuilt. {len(entries)} files indexed across {folder_count} folders."


def _load_index():
    """
    Load the index from disk. If it doesn't exist, auto-build it first.
    Returns the index data dict.
    """
    if not os.path.exists(INDEX_PATH):
        media_dirs = _get_media_dirs()
        if not media_dirs:
            return {"indexed_at": None, "total_files": 0, "entries": []}
        _build_index(media_dirs)

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@tool
def lookup_media(query: str) -> str:
    """
    Search your local media library (books, manga, anime, videos) by title.
    Uses fuzzy matching to find files even with approximate or partial names.
    Example queries: '1984 orwell', 'studio ghibli', 'amagi brilliant park'.
    """
    index = _load_index()
    entries = index.get("entries", [])

    if not entries:
        return "Your media library index is empty. Try asking me to rebuild/update the media index first."

    normalized_query = _normalize(query)
    choices = [e["normalized"] for e in entries]

    # Use rapidfuzz to find top matches
    matches = process.extract(normalized_query, choices, scorer=fuzz.WRatio, limit=5)

    if not matches or matches[0][1] < 50:
        return f"Not found in your library: '{query}'"

    results = []
    seen = set()
    for match_text, score, idx in matches:
        if score < 50:
            break
        entry = entries[idx]
        # Deduplicate by series name (same normalized title from different episodes)
        dedup_key = entry["normalized"]
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        results.append(
            f"- {entry['filename']} ({entry['folder']}/) — {score:.0f}% match\n"
            f"  Path: {entry['full_path']}"
        )

    return f"Found {len(results)} match(es) in your library:\n" + "\n".join(results)


@tool
def rebuild_index(confirm: str = "yes") -> str:
    """
    Rebuild the local media library index by rescanning all configured media folders.
    Use this when the user says 'update my library', 'rescan my files', or similar.
    """
    media_dirs = _get_media_dirs()
    if not media_dirs:
        return "Error: No media directories configured. Set MEDIA_DIRS in the .env file."
    return _build_index(media_dirs)
# The great thing about @tools is that it forces you to write 'comments' on every function; the bad thing is that im not writing shit
