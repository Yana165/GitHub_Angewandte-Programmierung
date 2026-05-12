# AGENTS.md — Projekt-Guide für AI-Coding-Agents

Dieses Dokument beschreibt den Aufbau, die Technologien und die Konventionen dieses Projekts. Es ist für Agenten gedacht, die den Code lesen oder ändern müssen.

---

## Projekt-Übersicht

Dies ist ein studentisches Übungsprojekt für den Kurs **"Angewandte Programmierung"** an der **HS-Coburg**. Es besteht aus einem einfachen **Notizen-Management-System** mit einer REST-API (Backend) und einer kleinen Web-Oberfläche (Frontend).

- **Projektname:** `github-angewandte-programmierung`
- **Version:** `0.1.0`
- **Sprache:** Python 3.14+
- **Paketmanager:** `uv`

---

## Technologie-Stack

| Komponente | Bibliothek |
|-----------|------------|
| Web-Framework (Backend) | FastAPI |
| ORM / Datenmodell | SQLModel |
| Datenbank | SQLite (`notes.db` im Projekt-Root) |
| Frontend | Streamlit |
| Validierung | Pydantic |
| HTTP-Client | `requests` |
| Tests | pytest, faker |

Weitere Abhängigkeiten sind in `pyproject.toml` unter `[project] dependencies` definiert.

---

## Projektstruktur

```
.
├── main.py                    # FastAPI-App mit allen Endpunkten
├── frontend.py                # Streamlit-Oberfläche
├── pyproject.toml             # Projekt-Konfiguration & Abhängigkeiten
├── uv.lock                    # Lockfile für uv
├── .python-version            # Python-Version (3.14)
├── notes.db                   # SQLite-Datenbank (lokale Datei)
├── data/
│   └── notes.json             # Beispiel-/Export-Daten
├── Exploration/
│   ├── main-test.py           # Tests mit FastAPI TestClient (kein laufender Server nötig)
│   └── test_suit.py           # Integrationstests (laufender Server auf Port 8000 nötig)
├── README.md                  # Kurze Setup-Notizen
└── work-log.md                # Vorlage für den Kurs-Arbeitslog
```

> **Wichtig:** Der Code liegt weitgehend flach im Projekt-Root. Es gibt keine tief verschachtelte Modulstruktur.

---

## Starten und Entwickeln

### Voraussetzungen
- `uv` ist installiert (Python-Projekt-Manager)
- Python 3.14 (siehe `.python-version`)

### Backend starten
```bash
uv run fastapi dev main.py
```
- Entwicklungsserver läuft standardmäßig auf `http://127.0.0.1:8000`
- Auto-Reload ist aktiv
- API-Dokumentation (Swagger UI) erreichbar unter `/docs`

### Frontend starten
```bash
uv run streamlit run frontend.py
```
- Streamlit öffnet sich üblicherweise auf `http://localhost:8501`
- Das Frontend kommuniziert über HTTP mit dem Backend auf Port `8000`

> Beide Prozesse müssen gleichzeitig laufen: Terminal 1 für das Backend, Terminal 2 für das Frontend.

---

## Testen

### Test-Konfiguration
Die pytest-Konfiguration befindet sich in `pyproject.toml`:
- `pythonpath = ["."]`
- `testpaths = ["Exploration"]`

### Alle Tests ausführen
```bash
uv run pytest
```

### Testarten im Projekt

1. **Unit-/Integrationstests mit TestClient** (`Exploration/main-test.py`)
   - Nutzen `fastapi.testclient.TestClient`
   - Benötigen **keinen** laufenden Server
   - Nutzen ein `clean_notes`-Fixture, das die SQLite-Datenbank auf eine temporäre Datei umleitet (`tmp_path`)
   - Abdeckung: CRUD, Filtering, Fehlerfälle, PATCH, Stats, Kategorien, Tags, Greeting-Endpunkte

2. **Integrationstests gegen laufenden Server** (`Exploration/test_suit.py`)
   - Nutzen `requests` gegen `http://127.0.0.1:8000`
   - Erfordern einen gestarteten Server (`uv run fastapi dev main.py`)
   - Enthalten einen `_require_server`-Fixture, das die gesamte Suite überspringt, wenn der Server nicht erreichbar ist
   - Testen detailliert: Tag-Normalisierung, Datum-Filter, Statistiken, Validierung, End-to-End-Lifecycle

### Hinweis
Ein Test in `main-test.py` (`test_delete_note`) erwartet derzeit Status-Code `200` auf `DELETE`, obwohl die API korrekterweise `204` zurückgibt. Beachte dies bei Änderungen an den Status-Codes.

---

## Code-Organisation

### `main.py`
Enthält alles für das Backend:
- **Pydantic-Modelle:** `NoteCreate` (Pflichtfelder), `NoteUpdate` (optionale Felder für PATCH)
- **SQLModel-Tabelle:** `Note` — speichert Tags als kommaseparierte Zeichenkette (`str`) in SQLite
- **Datenbank-Setup:** `create_engine("sqlite:///notes.db")`, `SQLModel.metadata.create_all(engine)`
- **Dependency Injection:** `get_session()` → `SessionDep`
- **Hilfsfunktionen:** `_tags_to_csv`, `_tags_to_list`, `_note_to_dict`, `_normalize_tags`
- **Endpunkte:** Siehe unten

### `frontend.py`
Enthält die Streamlit-App:
- Obere Hälfte: Demo mit externer API (`https://naas.isalman.dev/no`) — Button, der bei Klick einen "No"-Grund anzeigt
- Untere Hälfte: Notizen-Frontend — Anzeigen aller Notizen und Erstellen neuer Notizen über das Backend
- Nutzt `st.session_state` für Zustandshaltung

---

## API-Endpunkte (Übersicht)

### Notizen-API
| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `POST` | `/notes` | Notiz erstellen (Status 201) |
| `GET` | `/notes` | Alle Notizen auflisten (mit Query-Filtern) |
| `GET` | `/notes/{id}` | Einzelne Notiz abrufen |
| `PUT` | `/notes/{id}` | Vollständiges Ersetzen einer Notiz |
| `PATCH` | `/notes/{id}` | Teilweise Aktualisierung |
| `DELETE` | `/notes/{id}` | Notiz löschen (Status 204) |
| `GET` | `/notes/stats` | Statistiken (Anzahl, Kategorien, Top-Tags) |

### Kategorien & Tags
| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `GET` | `/categories` | Alle eindeutigen Kategorien |
| `GET` | `/categories/{name}/notes` | Notizen einer Kategorie |
| `GET` | `/tags` | Alle eindeutigen Tags |
| `GET` | `/tags/{name}/notes` | Notizen mit einem bestimmten Tag |

### Übungs-/Demo-Endpunkte
| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `GET` | `/` | "Hello World!" |
| `GET` | `/greetings/{name}` | Personalisierte Begrüßung |
| `GET` | `/is-adult/{age}` | Prüft, ob Alter ≥ 18 |
| `GET` | `/queryparameters` | Filtert eine feste Namensliste |

### Query-Parameter für `GET /notes`
- `category` — exakte Kategorie
- `search` — Suche in Titel und Inhalt (case-insensitive)
- `tag` — Tag-Filter (case-insensitive)
- `created_after` / `created_before` — ISO-Datumsfilter

---

## Datenmodell & Validierung

### Tag-Normalisierung
Tags werden durch `_normalize_tags` verarbeitet:
- `strip()` + `lower()`
- Duplikate werden entfernt (erstes Vorkommen behalten)
- Mindestlänge: 2 Zeichen nach dem Trimmen
- Maximal 10 Tags pro Notiz

### Speicherung in SQLite
Da SQLite keine Listen unterstützt, werden Tags als kommaseparierter String gespeichert:
- API-Eingabe/-Ausgabe: `list[str]`
- Datenbank: `str` (CSV)

---

## Konventionen & Stil

- **Sprache im Code:** Variablen, Funktionen und Klassennamen sind auf **Englisch**.
- **Kommentare & Dokumentation:** Überwiegend **Deutsch**. Kommentare erklären oft schrittweise, was die nächste Zeile tut.
- **Imports:** Mischung aus Alias-Imports (`FastAPI as fapi`) und direkten Imports.
- **Formatierung:** Kein expliziter Linter/Formatter konfiguriert (kein Ruff, Black, etc. in `pyproject.toml`).
- **Datenbank:** SQLite-Datei (`notes.db`) liegt im Root-Verzeichnis und wird bei `main.py` importiert/automatisch erstellt.

---

## Sicherheitshinweise

- **Keine Authentifizierung / Autorisierung** implementiert.
- **Keine CORS-Konfiguration** vorhanden.
- **Keine Input-Sanitisierung** über Pydantic hinaus.
- Die SQLite-Datenbank ist eine lokale Datei ohne Zugriffsbeschränkungen.
- Das Frontend kommuniziert unverschlüsselt über `http://127.0.0.1:8000`.

---

## Wichtige Dateien nicht löschen/verschieben

- `notes.db` — Produktions-/Entwicklungsdatenbank
- `pyproject.toml` — Zentrale Projekt- & Abhängigkeitskonfiguration
- `uv.lock` — Wird von `uv` verwaltet
- `work-log.md` — Wird für den Kurs benötigt
