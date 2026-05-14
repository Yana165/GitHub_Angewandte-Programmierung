from fastapi import FastAPI as fapi, HTTPException, Depends, Response
from pydantic import BaseModel, field_validator, model_validator, ConfigDict, ValidationError, Field as PydanticField
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, Annotated
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter
from typing_extensions import Self
import re


#### zum start der app und des frontends muss der mainserver laufen, dafür:
# - Terminal 1: uv run fastapi dev main.py
# schritt 2 ist das Frontend zu starten um zu sehen was geht, dafür:
# - Terminal 2: uv run streamlit run frontend.py

app = fapi(
    title = "Applied Programming Course HS-Coburg",
    description= "Simple note management API",
    version= "1.0.0"
)

###############################
#### Tag 1: Erste Einrichtung  ####
###############################
@app.get("/square/{number}")
def calculate_square(number: int):
    result = number * number
    return {
        "number": number,
        "square": result,
        "calculation": f"{number} × {number} = {result}"
    }


@app.get("/student")
def get_student():
    return {
        "name": "Yana Zimmer",
        "semester": 2,
        "course": "Wirtschaftsinformatik",
        "university": "HS Coburg"
    }


@app.get("/double/{number}")
def calculate_double(number: int):
    result = number * 2
    return {
        "number": number,
        "double": result,
        "calculation": f"{number} × 2 = {result}"
    }




##################################
#### Note API Endpoints Day 2 ####
##################################

ALLOWED_CATEGORIES = {"work", "personal", "school", "ideas", "general"}


def _normalize_tags(v: list[str]) -> list[str]:
    """Strip + lowercase + dedupe. Reject tags shorter than 2 chars or more than 10 entries."""
    seen = set()
    result = []
    for tag in v:
        normalized = tag.strip().lower()
        if len(normalized) < 2:
            raise ValueError("each tag must be at least 2 characters after trimming")
        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    if len(result) > 10:
        raise ValueError("at most 10 tags allowed per note")
    return result


class NoteCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    title: str = PydanticField(
        min_length=3,
        max_length=100,
        description="Short note title shown in lists",
    )
    content: str = PydanticField(
        min_length=1,
        max_length=10_000,
        description="Note body content",
    )
    category: str = PydanticField(
        min_length=2,
        max_length=30,
        pattern=r"^[a-z]+$",
        description="Lowercase category, e.g. work, personal, school",
    )
    tags: list[str] = PydanticField(
        default_factory=list,
        max_length=10,
        description="Up to 10 lowercase tags",
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Reject titles that are only whitespace after stripping."""
        v = v.strip()
        if len(v) < 3:
            raise ValueError("title must be at least 3 characters after trimming")
        return v

    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, v: str) -> str:
        """Normalize to lowercase and restrict to allowed values."""
        v = v.strip().lower()
        if v not in ALLOWED_CATEGORIES:
            raise ValueError(f"category must be one of {sorted(ALLOWED_CATEGORIES)}")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Strip + lowercase each tag, drop duplicates, reject empty/short tags."""
        return _normalize_tags(v)

    @model_validator(mode="after")
    def work_notes_need_work_tag(self) -> Self:
        """
        Cross-field rule: work notes must include the 'work' tag.
        This must be a model validator because it accesses multiple fields (category + tags).
        """
        if self.category == "work" and "work" not in self.tags:
            raise ValueError("work notes must include the 'work' tag")
        return self


class NoteUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    title: str | None = PydanticField(default=None, min_length=3, max_length=100)
    content: str | None = PydanticField(default=None, min_length=1, max_length=10_000)
    category: str | None = PydanticField(
        default=None, min_length=2, max_length=30, pattern=r"^[a-z]+$"
    )
    tags: list[str] | None = PydanticField(default=None, max_length=10)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if len(v) < 3:
            raise ValueError("title must be at least 3 characters after trimming")
        return v

    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().lower()
        if v not in ALLOWED_CATEGORIES:
            raise ValueError(f"category must be one of {sorted(ALLOWED_CATEGORIES)}")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        return _normalize_tags(v)

    @model_validator(mode="after")
    def work_notes_need_work_tag(self) -> Self:
        """Cross-field rule: if category becomes work, the work tag must be present."""
        if self.category == "work" and self.tags is not None and "work" not in self.tags:
            raise ValueError("work notes must include the 'work' tag")
        return self


# Pure Pydantic model for tag validation (no DB table)
class Tag(BaseModel):
    """Validation-only model for tag names."""

    name: str = PydanticField(min_length=2, max_length=30)

    @field_validator("name")
    @classmethod
    def clean_name(cls, v: str) -> str:
        """Strip, lowercase and restrict to lowercase letters, digits and hyphens."""
        v = v.strip().lower()
        if not re.match(r"^[a-z0-9-]+$", v):
            raise ValueError("tag name must be lowercase letters, digits or hyphens")
        return v


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
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
) -> list[dict]:
    """List notes with optional filters"""
    notes_db = session.exec(select(Note)).all()

    tag_lower = tag.lower() if tag else None
    after_iso = created_after.isoformat() if created_after else None
    before_iso = created_before.isoformat() if created_before else None

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
        if tag_lower and tag_lower not in tag_list:
            continue

        if after_iso and note.created_at < after_iso:
            continue

        if before_iso and note.created_at > before_iso:
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


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    """Delete a note by ID. Returns 204 No Content."""
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")
    session.delete(note)
    session.commit()
    return Response(status_code=204)


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


@app.get("/tags")
def list_tags(session: SessionDep) -> list[str]:
    """Get all unique tags across all notes (sorted)."""
    notes_db = session.exec(select(Note)).all()
    all_tags = set()
    for note in notes_db:
        all_tags.update(_tags_to_list(note.tags))
    return sorted(all_tags)


@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str, session: SessionDep) -> list[dict]:
    """Get all notes carrying a given tag (case-insensitive)."""
    tag_lower = tag_name.lower()
    notes_db = session.exec(select(Note)).all()
    return [
        _note_to_dict(note)
        for note in notes_db
        if tag_lower in _tags_to_list(note.tags)
    ]


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
