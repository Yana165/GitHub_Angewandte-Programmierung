import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlmodel import SQLModel, create_engine
import main
from main import app, Tag



# TestClient ermöglicht es, HTTP-Anfragen an die FastAPI-Anwendung zu senden, ohne einen echten Server zu starten. 
# Dadurch können wir die Endpunkte direkt testen und die Antworten überprüfen. 
# In diesem Testcode verwenden wir TestClient, um verschiedene Szenarien für die Notizen-API zu testen, z.B. das 
# Erstellen von Notizen mit ungültigen Daten, das Aktualisieren von Notizen, und die Validierung von Tags.

client = TestClient(app)


@pytest.fixture
def clean_notes(tmp_path, monkeypatch):
    """Redirect the SQLite engine to a temp .db so notes-tests don't touch real data"""
    temp_db = tmp_path / "notes.db"
    test_engine = create_engine(f"sqlite:///{temp_db}")
    SQLModel.metadata.create_all(test_engine)
    monkeypatch.setattr(main, "engine", test_engine)
    yield temp_db


def test_create_note_rejects_short_title(clean_notes):  # clean_notes ist ein pytest fixture, das sicherstellt, dass die Tests mit einer sauberen Datenbank arbeiten, um unerwünschte Wechselwirkungen zwischen Tests zu vermeiden.
    """POST /notes with title shorter than 3 chars must return 422."""
    response = client.post("/notes", json={
        "title": "ab",
        "content": "Valid content",
        "category": "general",
        "tags": [],
    })
    assert response.status_code == 422 


def test_create_note_rejects_unknown_category(clean_notes):
    """POST /notes with an unknown category must return 422."""
    response = client.post("/notes", json={
        "title": "Valid title",
        "content": "Valid content",
        "category": "banana",
        "tags": [],
    })
    assert response.status_code == 422    


def test_create_note_normalizes_tags(clean_notes):
    """Tags should be lowercased, stripped and deduplicated."""
    response = client.post("/notes", json={
        "title": "Tag normalization test",
        "content": "Valid content",
        "category": "general",
        "tags": ["URGENT", "urgent", "  meeting  ", "Q2"],
    })
    assert response.status_code == 201
    data = response.json()
    assert sorted(data["tags"]) == sorted(["urgent", "meeting", "q2"])


def test_create_note_forbids_extra_fields(clean_notes):     # Dieser Test überprüft, ob die API korrekt auf ungültige Eingaben reagiert, indem er versucht, eine Notiz mit einem zusätzlichen Feld (tagz statt tags) zu erstellen. 
    """POST /notes with an extra field (typo) must return 422 because extra='forbid'."""
    response = client.post("/notes", json={
        "title": "Valid title",
        "content": "Valid content",
        "category": "general",
        "tags": [],
        "tagz": ["typo"],
    })
    assert response.status_code == 422


def test_work_note_requires_work_tag(clean_notes):
    """POST /notes with category='work' but without 'work' tag must return 422."""
    response_fail = client.post("/notes", json={
        "title": "Work note without work tag",
        "content": "Valid content",
        "category": "work",
        "tags": [],
    })
    assert response_fail.status_code == 422     # ValidationError wegen @root_validator

    response_ok = client.post("/notes", json={
        "title": "Work note with work tag",
        "content": "Valid content",
        "category": "work",
        "tags": ["work"],
    })
    assert response_ok.status_code == 201


def test_patch_with_empty_body_succeeds(clean_notes):
    """PATCH /notes/{id} with {} must succeed and leave fields unchanged."""
    create_resp = client.post("/notes", json={
        "title": "Original title",
        "content": "Original content",
        "category": "general",
        "tags": ["original"],
    })
    assert create_resp.status_code == 201
    note_id = create_resp.json()["id"]

    patch_resp = client.patch(f"/notes/{note_id}", json={})
    assert patch_resp.status_code == 200
    data = patch_resp.json()
    assert data["title"] == "Original title"
    assert data["content"] == "Original content"
    assert data["category"] == "general"
    assert data["tags"] == ["original"]


def test_patch_with_invalid_title_fails(clean_notes):               
    """PATCH /notes/{id} with an invalid title must return 422."""
    create_resp = client.post("/notes", json={
        "title": "Valid title",
        "content": "Valid content",
        "category": "general",
        "tags": [],
    })
    assert create_resp.status_code == 201
    note_id = create_resp.json()["id"]

    patch_resp = client.patch(f"/notes/{note_id}", json={"title": ""})
    assert patch_resp.status_code == 422


def test_tag_name_rejects_uppercase(clean_notes):
    """Tag model must reject names containing invalid characters (e.g. spaces)."""
    with pytest.raises(ValidationError):
        Tag(name="UPPER CASE")  # Großbuchstaben sind nicht erlaubt, da regex="^[a-z0-9]+$" in Tag definiert ist
