from fastapi import FastAPI as fapi, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import json
from pathlib import Path
from collections import Counter

##################################
#### Endpoints Day 1 ####
##################################


#app = fapi()

#@app.get("/name/{name}")
#def greet_name(name:str): 
 #   return {"message": f"Hello, {name}!"}



##################################
#### Note API Endpoints Day 2 ####
##################################



app = fapi(
    title = "Applied Programming Course HS-Coburg",
    description= "Simple note management API",
    version= "1.0.0" 
)


class NoteCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str] = []

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None

class Note(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str] = []
    created_at: str

NOTES_FILE = Path("data/notes.json")

def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    note_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            # Set counter to max ID + 1
            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, note_id_counter


def save_notes(notes_db):
    """Save notes to JSON file after each change"""
    # Ensure data directory exists
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, 'w') as f:
        # Convert Note objects to dicts
        notes_data = [note.model_dump() for note in notes_db]
        json.dump(notes_data, f, indent=2)


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate) -> Note:

    """Create a new note"""

    notes_db, note_id_counter = load_notes()

    new_note = Note(
        id=note_id_counter,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=note.tags,
        created_at=datetime.now(timezone.utc).isoformat()
    )

    notes_db.append(new_note)
    save_notes(notes_db)


    return new_note

@app.get("/notes")
def list_notes(
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None,
) -> list[Note]:
    """List notes with optional filters"""
    notes_db, _ = load_notes()

    filtered = []
    for note in notes_db:
        if category and note.category != category:
            continue

        if search:
            search_lower = search.lower()
            title_match = search_lower in note.title.lower()
            content_match = search_lower in note.content.lower()
            if not (title_match or content_match):
                continue

        if tag and tag not in note.tags:
            continue

        if created_after and note.created_at < created_after:
            continue

        if created_before and note.created_at > created_before:
            continue

        filtered.append(note)

    return filtered


 


##################################
#### Statistic Endpoints Day 3 ####
##################################

##################################
#### Pytests Endpoints Day 4 ####
##################################

##################################
####  Endpoints Day 5 ####
##################################