import json
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.notes_manager import *
from typing import Any
from dotenv import load_dotenv      

load_dotenv()

TOOLS = {
    "add_note": add_note,
    "read_notes": read_notes,
    "get_latest": get_latest,
    "edit_note": edit_note,
    "delete_note": delete_note,
    "search_notes": search_notes,
    "list_tags": list_tags,
    "notes_by_tag": notes_by_tag,
}

SYSTEM_PROMPT = """
You are an AI assistant for a note-taking system. 
You can call these tools with JSON output:

- add_note(message: str, tags: list[str]="")
- read_notes()
- get_latest()
- edit_note(note_id: str, new_text: str)
- delete_note(note_id: str)
- search_notes(query: str)
- list_tags()
- notes_by_tag(tag: str)

Only respond with JSON {"tool": "...", "args": {...}}.
"""

def interpret(user_input: str) -> Any:
    model = ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite')
    res = model.chat(system=SYSTEM_PROMPT, messages=[{"role":"user","content":user_input}])
    try:
        c = json.loads(res.content)
        fn = TOOLS[c["tool"]]
        result = fn(**c.get("args", {}))
        return result
    except Exception as e:
        return {"error": f"Failed to interpret: {e}"}
