from fastapi import FastAPI as fapi, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import json
from pathlib import Path
from sqlmodel import SQLModel, Field, Session, create_engine, select
from collections import Counter
from typing import Optional

##################################
#### Endpoints Day 1          ####
##################################


#app = fapi()

#@app.get("/name/{name}")
#def greet_name(name:str): 
    #return {"message": f"Hello, {name}!"}



##################################
#### Note API Endpoints Day 2 ####
##################################

engine = create_engine("sqlite:///notes.db", echo=True)

SQLModel.metadata.create_all(engine)


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


@app.get("/notes/stats")
def get_note_stats():
    """Get statistics about all notes"""
    notes_db, _ = load_notes()

    by_category = {}
    tag_counter = Counter()

    for note in notes_db:
        by_category[note.category] = by_category.get(note.category, 0) + 1
        for tag in note.tags:
            tag_counter[tag] += 1

    top_tags = [{"tag": tag, "count": count} for tag, count in tag_counter.most_common(5)]

    return {
        "total_notes": len(notes_db),
        "by_category": by_category,
        "top_tags": top_tags,
        "unique_tags_count": len(tag_counter),
    }

@app.get("/notes/{note_id}")
def get_note(note_id: int) -> Note:
    """Get a specific note by ID"""
    notes_db, _ = load_notes()

    for note in notes_db:
        if note.id == note_id:
            return note

    raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")


@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate) -> Note:
    """Replace all fields of a note (full update)"""
    notes_db, _ = load_notes()

    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated = Note(
                id=note.id,
                title=note_update.title,
                content=note_update.content,
                category=note_update.category,
                tags=note_update.tags,
                created_at=note.created_at,
            )
            notes_db[i] = updated
            save_notes(notes_db)
            return updated

    raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    """Delete a note by ID"""
    notes_db, _ = load_notes()

    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)
            save_notes(notes_db)
            return {"message": f"Note {note_id} deleted"}

    raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")


@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate) -> Note:
    """Partially update a note — only provided fields are changed"""
    notes_db, _ = load_notes()

    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated = Note(
                id=note.id,
                title=note_update.title if note_update.title is not None else note.title,
                content=note_update.content if note_update.content is not None else note.content,
                category=note_update.category if note_update.category is not None else note.category,
                tags=note_update.tags if note_update.tags is not None else note.tags,
                created_at=note.created_at,
            )
            notes_db[i] = updated
            save_notes(notes_db)
            return updated

    raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")


@app.get("/categories")
def list_categories() -> list[str]:
    """Get all unique categories from all notes"""
    notes_db, _ = load_notes()
    return sorted({note.category for note in notes_db})


@app.get("/categories/{category_name}/notes")
def get_notes_by_category(category_name: str) -> list[Note]:
    """Get all notes in a specific category"""
    notes_db, _ = load_notes()
    return [note for note in notes_db if note.category == category_name]


##################################
#### Statistic Endpoints Day 3 ###
##################################

@app.get("/queryparameters")
def get_query_parameters(param1: str, param2: int) -> dict:

        namen = ['martin', 'michael', 'sarah', 'anna', 'tom', 'lisa']

        if not param1:
              return{"namen": namen}

        namen_gefiltert = []
        for name in namen:
                if param1 in name:
                 namen_gefiltert.append(name)
        return {"param1": param1, "param2": param2, "filtered_names": namen_gefiltert}


##################################
#### Day 4: Greeting Endpoints TESTING ###
##################################

class GreetingResponse(BaseModel):
    """Response model for greeting endpoints

    Attributes:
        message (str): The greeting message to be returned to the client
    """
    message: str


@app.get("/", response_model=GreetingResponse)
def read_root():
    """Welcome endpoint - returns greeting message"""
    return {"message": "Hello World!"}




@app.get("/greetings/{name}", response_model=GreetingResponse)
def read_greeting(name: str):
    """Personalized greeting endpoint - returns greeting message with name"""
    return {"message": f"Hello {name}!"}


@app.get("/is-adult/{age}")
def check_adult(age: int):
    """
    Check if person is an adult (18 or older)
    Example: /is-adult/17
    """
    is_adult = age >= 18

    return {
        "age": age,
        "is_adult": is_adult,
        "can_vote": is_adult,
        "can_drive": is_adult
    }

##################################
####  Endpoints Day 5         ####
##################################

##################################
####  Endpoints Day 6         ####
##################################