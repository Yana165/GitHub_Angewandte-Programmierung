# 📝 Notizen-Management System

Ein einfaches **Notizen-Management-System** für den Kurs "Angewandte Programmierung" an der HS Coburg. 
Das Projekt kombiniert eine **FastAPI Backend** mit einer **Streamlit Frontend** und verwendet **SQLModel** für die Datenverwaltung.

---

## 🚀 Features

- ✅ **REST-API** mit FastAPI für vollständige CRUD-Operationen
- ✅ **SQLite-Datenbank** für persistente Datenspeicherung
- ✅ **Web-Interface** mit Streamlit
- ✅ **Tag- & Kategorie-System** zur Organisierung von Notizen
- ✅ **Filterfunktionen** (nach Kategorie, Tag, Inhalt, Datum)
- ✅ **Statistiken** über Notizen und Tags
- ✅ **Vollständig getestet** mit pytest

---

## 📋 Technologie-Stack

| Komponente | Technologie |
|-----------|------------|
| **Backend Framework** | FastAPI |
| **ORM/Datenmodell** | SQLModel |
| **Datenbank** | SQLite |
| **Frontend** | Streamlit |
| **Validierung** | Pydantic |
| **Paketmanager** | `uv` |
| **Tests** | pytest, faker |

---

## 🛠️ Installation & Setup

### Voraussetzungen
- Python 3.14+
- `uv` Paketmanager ([Installation](https://docs.astral.sh/uv/))

### Projekt klonen
```bash
git clone https://github.com/Yana165/GitHub_Angewandte-Programmierung.git
cd GitHub_Angewandte-Programmierung
```

### Dependencies installieren
```bash
uv sync
```

---

## ▶️ Anwendung starten

### Backend starten (Terminal 1)
```bash
uv run fastapi dev main.py
```
- Server läuft auf: `http://127.0.0.1:8000`
- API-Dokumentation: `http://127.0.0.1:8000/docs`

### Frontend starten (Terminal 2)
```bash
uv run streamlit run frontend.py
```
- Frontend öffnet sich automatisch unter `http://localhost:8501`

> **Hinweis:** Beide Prozesse müssen gleichzeitig laufen!

---

## 📚 API-Endpunkte

### Notizen CRUD
| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `POST` | `/notes` | Notiz erstellen |
| `GET` | `/notes` | Alle Notizen auflisten |
| `GET` | `/notes/{id}` | Einzelne Notiz abrufen |
| `PUT` | `/notes/{id}` | Notiz vollständig ersetzen |
| `PATCH` | `/notes/{id}` | Notiz teilweise aktualisieren |
| `DELETE` | `/notes/{id}` | Notiz löschen |

### Kategorien & Tags
| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `GET` | `/categories` | Alle Kategorien auflisten |
| `GET` | `/categories/{name}/notes` | Notizen einer Kategorie |
| `GET` | `/tags` | Alle Tags auflisten |
| `GET` | `/tags/{name}/notes` | Notizen mit bestimmtem Tag |

### Sonstige Endpunkte
| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `GET` | `/notes/stats` | Statistiken über Notizen |
| `GET` | `/` | Willkommen-Nachricht |
| `GET` | `/greetings/{name}` | Personalisierte Begrüßung |

---

## 🧪 Tests ausführen

```bash
# Alle Tests ausführen
uv run pytest

# Mit verbosem Output
uv run pytest -v

# Mit Coverage
uv run pytest --cov
```

---

## 📁 Projektstruktur

```
.
├── main.py                    # FastAPI-Backend mit allen Endpunkten
├── frontend.py                # Streamlit-Web-Interface
├── pyproject.toml             # Projekt-Konfiguration & Dependencies
├── notes.db                   # SQLite-Datenbank (wird auto. erstellt)
├── data/
│   └── notes.json             # Beispiel-Daten
├── Exploration/
│   ├── main-test.py           # Unit-Tests mit TestClient
│   ├── test_suit.py           # Integrationstests
│   └── test_validation.py     # Validierungstests
└── README.md                  # Diese Datei
```

---

## 💾 Datenmodell

### Note (Notiz)
```python
{
  "id": 1,
  "title": "Beispiel",
  "content": "Notizinhalt",
  "category": "work",
  "tags": ["python", "fastapi"],
  "created_at": "2026-05-14T10:30:00Z"
}
```

### Erlaubte Kategorien
`work`, `personal`, `school`, `ideas`, `general`

---

## 🎓 Kurs-Kontext

Dieses Projekt ist Teil des Kurses **"Angewandte Programmierung"** (2. Semester Wirtschaftsinformatik) an der **HS Coburg**.

---

## 📝 Lizenz

MIT License - Siehe `LICENSE` für Details.

---

## 👤 Autor

**Yana Zimmer**  
HS Coburg - Wirtschaftsinformatik (2. Semester)
