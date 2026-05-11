from fastapi import FastAPI as fapi, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, Annotated
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

app = fapi(
    title = "Applied Programming Course HS-Coburg",
    description= "Simple note management API",
    version= "1.0.0"
)

##################################
#### Note API Endpoints Day 2 ####
##################################

# Pydantic models for request bodies (tags as list)
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


# SQLModel table: tags stored as CSV string (SQLite has no array type)
class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    tags: str = ""
    created_at: str


# DB setup
DB_FILE = Path("notes.db")
engine = create_engine(f"sqlite:///{DB_FILE}")
SQLModel.metadata.create_all(engine)


def get_session():
    """Yields a DB session per request; closes automatically afterwards."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# Helpers: convert between CSV string (DB) and list (API)
def _tags_to_csv(tags: list[str]) -> str:
    return ",".join(tags)

def _tags_to_list(tags_csv: str) -> list[str]:
    return tags_csv.split(",") if tags_csv else []

def _note_to_dict(note: Note) -> dict:
    """Convert a DB Note into the API response shape (tags as list)."""
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "category": note.category,
        "tags": _tags_to_list(note.tags),
        "created_at": note.created_at,
    }


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: SessionDep) -> dict:
    """Create a new note"""
    new_note = Note(
        title=note.title,
        content=note.content,
        category=note.category,
        tags=_tags_to_csv(note.tags),
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    return _note_to_dict(new_note)


@app.get("/notes")
def list_notes(
    session: SessionDep,
    category: Optional[str] = None,
    search: Optional[str] = None,
    tag: Optional[str] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
) -> list[dict]:
    """List notes with optional filters"""
    notes_db = session.exec(select(Note)).all()

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

        tag_list = _tags_to_list(note.tags)
        if tag and tag not in tag_list:
            continue

        if created_after and note.created_at < created_after:
            continue

        if created_before and note.created_at > created_before:
            continue

        filtered.append(_note_to_dict(note))

    return filtered


@app.get("/notes/stats")
def get_note_stats(session: SessionDep):
    """Get statistics about all notes"""
    notes_db = session.exec(select(Note)).all()

    by_category = {}
    tag_counter = Counter()

    for note in notes_db:
        by_category[note.category] = by_category.get(note.category, 0) + 1
        for tag in _tags_to_list(note.tags):
            tag_counter[tag] += 1

    top_tags = [{"tag": tag, "count": count} for tag, count in tag_counter.most_common(5)]

    return {
        "total_notes": len(notes_db),
        "by_category": by_category,
        "top_tags": top_tags,
        "unique_tags_count": len(tag_counter),
    }


@app.get("/notes/{note_id}")
def get_note(note_id: int, session: SessionDep) -> dict:
    """Get a specific note by ID"""
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")
    return _note_to_dict(note)


@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate, session: SessionDep) -> dict:
    """Replace all fields of a note (full update)"""
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

    note.title = note_update.title
    note.content = note_update.content
    note.category = note_update.category
    note.tags = _tags_to_csv(note_update.tags)

    session.add(note)
    session.commit()
    session.refresh(note)
    return _note_to_dict(note)


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, session: SessionDep):
    """Delete a note by ID"""
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")
    session.delete(note)
    session.commit()
    return {"message": f"Note {note_id} deleted"}


@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate, session: SessionDep) -> dict:
    """Partially update a note — only provided fields are changed"""
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content
    if note_update.category is not None:
        note.category = note_update.category
    if note_update.tags is not None:
        note.tags = _tags_to_csv(note_update.tags)

    session.add(note)
    session.commit()
    session.refresh(note)
    return _note_to_dict(note)


@app.get("/categories")
def list_categories(session: SessionDep) -> list[str]:
    """Get all unique categories from all notes"""
    notes_db = session.exec(select(Note)).all()
    return sorted({note.category for note in notes_db})


@app.get("/categories/{category_name}/notes")
def get_notes_by_category(category_name: str, session: SessionDep) -> list[dict]:
    """Get all notes in a specific category"""
    notes_db = session.exec(select(Note).where(Note.category == category_name)).all()
    return [_note_to_dict(note) for note in notes_db]


##################################
#### Day 3: Query Parameters #####
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
#### Day 4: Greeting Endpoints ###
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