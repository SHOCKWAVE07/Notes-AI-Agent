import os, json, uuid, datetime

NOTES_FILE = "notes.json"

def ensure():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            json.dump([], f)

def load():
    ensure()
    return json.load(open(NOTES_FILE))

def save(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def add_note(message, tags=None):
    notes = load()
    note = {
        "id": str(uuid.uuid4()),
        "text": message,
        "tags": tags or [],
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": None,
    }
    notes.append(note)
    save(notes)
    return {"message": "Note added.", "note": note}

def read_notes():
    return load()

def get_latest():
    notes = load()
    return max(notes, key=lambda x: x["created_at"], default=None)

def edit_note(note_id, new_text):
    notes = load()
    for n in notes:
        if n["id"] == note_id:
            n["text"] = new_text
            n["updated_at"] = datetime.datetime.now().isoformat()
            save(notes)
            return {"message": "Note updated.", "note": n}
    return {"message": "Note not found."}

def delete_note(note_id):
    notes = load()
    notes2 = [n for n in notes if n["id"] != note_id]
    if len(notes2) < len(notes):
        save(notes2)
        return {"message": "Note deleted."}
    return {"message": "Note not found."}

def search_notes(query):
    return [n for n in load() if query.lower() in n["text"].lower()]

def list_tags():
    notes = load()
    return list({tag for n in notes for tag in n["tags"]})

def notes_by_tag(tag):
    return [n for n in load() if tag in n["tags"]]
