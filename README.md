# 📝 Notizen-Management System – Lern- & Entwicklungsprojekt

Dieses Projekt ist ein umfassendes Lern- und Entwicklungsprojekt für den Kurs **"Angewandte Programmierung"** (2. Semester Wirtschaftsinformatik) an der **HS Coburg**. 

Es dokumentiert den **vollständigen Weg vom Zero zum selbstständig funktionierenden System**: von der ersten FastAPI-Installation über REST-API-Design, Datenbankintegration mit SQLModel, umfassender Validierung mit Pydantic, automatisiertem Testen mit pytest bis hin zur Weboberfläche mit Streamlit.

---

## 📚 Projekt-Dokumentation

### Hauptdokumentation
- **[`work-log.md`](work-log.md)** — Detailliertes Lerntagebuch mit täglicher Reflektion:
  - 7 Tage Kurssitzungen mit Herausforderungen, Lernzielen und Lösungsansätzen
  - Persönliche Erfahrungen und technische Deep-Dives
  - Ideale Ressource für Studenten, die ähnliche Konzepte lernen

### Technische Dokumentation
- **[`README.md`](README.md)** — Technische Projektübersicht und Quick-Start
- **[`AGENTS.md`](AGENTS.md)** — Vollständiger technischer Guide für AI-Coding-Agents

---

## 🎯 Lernziele

Dieses Projekt führt systematisch durch folgende Konzepte:

| Woche | Thema | Kernkonzepte |
|-------|-------|--------------|
| **1** | FastAPI & REST-Grundlagen | HTTP-Methoden, Endpunkte, JSON, Pfad-Parameter |
| **1** | Python-Grundlagen & Persistierung | Datentypen, JSON-Dateiverwaltung, ID-Verwaltung |
| **1** | REST-API-Design | CRUD, Filterung, Ressourcen-Navigation, Query-Parameter |
| **2** | Testing & Validierung | pytest, TestClient, Pydantic-Constraints, Custom Validators |
| **2** | Datenbankintegration | SQLModel, SQLite, Many-to-Many-Beziehungen, Session-Management |
| **3** | Python-Decorators | Decorator-Muster, Refactoring, Debugging |
| **3** | Frontend-Entwicklung | Streamlit, Session State, Multi-Process-Workflows |

---

## 🚀 Quick Start

### Backend starten
```bash
# Installation
uv sync  # Installiert alle Dependencies

# Server starten
uv run fastapi dev main.py
```
✅ Backend läuft auf `http://127.0.0.1:8000`  
📚 API-Docs unter `http://127.0.0.1:8000/docs`

### Frontend starten (zweites Terminal)
```bash
uv run streamlit run frontend.py
```
✅ Frontend öffnet sich automatisch unter `http://localhost:8501`

### Tests ausführen
```bash
uv run pytest -v                    # Alle Tests
uv run pytest -v -k "test_name"     # Spezifischer Test
uv run pytest --cov                 # Mit Coverage
```

---

## 🏗️ Projektstruktur

```
.
├── main.py                    # FastAPI Backend (alle Endpunkte)
├── frontend.py                # Streamlit Web-UI
├── pyproject.toml             # Projekt-Config & Dependencies
├── work-log.md                # 📖 LERNTAGEBUCH (Detaillierte Reflexion)
├── README.md                  # Technische Übersicht
├── AGENTS.md                  # AI-Agent Guide
├── notes.db                   # SQLite-Datenbank
├── Exploration/
│   ├── main-test.py           # Unit-Tests (TestClient, kein Server nötig)
│   ├── test_suit.py           # Integrationstests (mit laufendem Server)
│   └── test_validation.py     # Validierungs-spezifische Tests
└── data/
    └── notes.json             # Beispiel-Daten
```

---

## 📖 Wie man dieses Projekt nutzt

### 📚 Zum Lernen
1. **Starten Sie mit [`work-log.md`](work-log.md)**  
   Lesen Sie die Lerneinträge Tag für Tag, um zu verstehen:
   - Was wurde gelernt?
   - Welche Herausforderungen traten auf?
   - Wie wurden sie gelöst?

2. **Parallel: Code durchgehen**  
   - Öffnen Sie `main.py` und sehen Sie die endgültige Implementierung
   - Vergleichen Sie mit den Etappen aus dem Worklog
   - Führen Sie Tests aus, um Verhalten zu verstehen

3. **Hands-On: Reproduzieren Sie die Schritte**  
   - Starten Sie Frontend und Backend gleichzeitig
   - Erstellen Sie Notizen, beobachten Sie die Validierung
   - Schauen Sie sich die Datenbank-Struktur an

### 👨‍💻 Zum Erweitern
- Neue Endpunkte in `main.py` hinzufügen
- Validierungs-Regeln verschärfen/anpassen
- Frontend mit zusätzlichen Features erweitern
- Tests für neue Features schreiben

### 🤖 Für AI-Coding-Agenten
Konsultieren Sie [`AGENTS.md`](AGENTS.md) für:
- Vollständige Projekt-Architektur
- Konventionen und Code-Stil
- Testing-Setup und Konfiguration
- API-Endpunkt-Spezifikation

---

## 🔑 Zentrale Technologien

| Tool | Rolle | Version |
|------|-------|---------|
| **FastAPI** | Web-Framework & REST-API | 0.136.1+ |
| **SQLModel** | ORM & Datenbankmodelle | 0.0.38+ |
| **Pydantic** | Datenvalidierung | 2.x |
| **SQLite** | Persistente Datenbank | Built-in |
| **Streamlit** | Web-Frontend | Latest |
| **pytest** | Automated Testing | 9.0.3+ |
| **uv** | Paketmanager | Latest |

---

## 📝 API-Übersicht

### Notizen verwalten
- `POST /notes` — Neue Notiz erstellen (Status 201)
- `GET /notes` — Alle Notizen (mit Filterung)
- `GET /notes/{id}` — Spezifische Notiz abrufen
- `PUT /notes/{id}` — Notiz vollständig ersetzen
- `PATCH /notes/{id}` — Notiz teilweise aktualisieren
- `DELETE /notes/{id}` — Notiz löschen (Status 204)

### Kategorien & Tags
- `GET /categories` — Alle verfügbaren Kategorien
- `GET /categories/{name}/notes` — Notizen einer Kategorie
- `GET /tags` — Alle verfügbaren Tags
- `GET /tags/{name}/notes` — Notizen mit bestimmtem Tag

### Statistiken & Utility
- `GET /notes/stats` — Statistiken (Anzahl, Top-Tags, Kategorien)
- `GET /` — Willkommen-Nachricht
- `GET /greetings/{name}` — Personalisierte Begrüßung

---

## 🧪 Testing-Strategie

Das Projekt nutzt zwei Test-Ansätze:

### 1️⃣ Unit-Tests mit TestClient (`main-test.py`)
- ✅ Kein Server nötig, schnell
- ✅ Isolierte Tests mit `tmp_path` Fixture
- ✅ Ideale für lokale Entwicklung

```bash
uv run pytest Exploration/main-test.py -v
```

### 2️⃣ Integrationstests gegen Server (`test_suit.py`)
- ✅ Testet echtes HTTP-Verhalten
- ✅ Validiert Real-World-Szenarien
- ⚠️ Benötigt laufenden Server

```bash
# Terminal 1: Backend starten
uv run fastapi dev main.py

# Terminal 2: Tests ausführen
uv run pytest Exploration/test_suit.py -v
```

---

## 🎓 Lernressourcen im Code

### Kommentierte Konzepte
Die folgenden Dateien enthalten ausführliche Inline-Kommentare zu Konzepten:

| Datei | Konzept | Lerne |
|-------|---------|-------|
| `main.py` | SQLModel, Dependency Injection, Validierung | Datenbankabstraktionen, Session-Management |
| `frontend.py` | Streamlit State Management, Multi-Request | Reactive Web-Frameworks |
| `Exploration/main-test.py` | TestClient, Mocking, Isolation | Automated Testing Patterns |
| `Exploration/test_suit.py` | Integration Tests, Server Lifecycle | End-to-End Testing |

### Debug-Tipps
```python
# Verhalten schnell testen:
uv run python -c "from main import app; print(app.routes)"

# SQLite-DB inspizieren (VS Code SQLite Extension):
# Rechtsklick auf notes.db → "Open Database"

# Streamlit Session Debuggen:
# st.write(st.session_state)
```

---

## 📊 Projektmetriken

| Metrik | Wert |
|--------|------|
| **Codezeilen** (main.py) | ~400 |
| **Test-Cases** | 50+ |
| **Endpunkte** | 15+ |
| **API-Validierungen** | 20+ Custom Rules |
| **Lerneinträge** | 7 Tage × 3 Sektionen |
| **Technologien** | 7 Kern-Biblioteken |

---

## 🤝 Beiträge & Erweiterungen

Dieses Projekt ist als Lerngrundlage konzipiert. Mögliche Erweiterungen:

- [ ] **Authentifizierung** — JWT-basierte User-Sessions
- [ ] **Autorisierung** — Rollenbasierte Zugriffskontrolle (RBAC)
- [ ] **API-Versionierung** — `/v1/`, `/v2/` Endpunkte
- [ ] **Caching** — Redis-Integration für Performance
- [ ] **Logging** — Structlog für Production-Grade Logs
- [ ] **Docker** — Containerisierung für Deployment
- [ ] **Docker Compose** — Multi-Container Orchestration
- [ ] **WebSockets** — Echtzeit-Notizen-Aktualisierungen
- [ ] **GraphQL** — Alternative zu REST API

---

## ⚠️ Hinweise für Production

Dieses Projekt ist **Educationals / Lernprojekt**. Für Production:

❌ **Nicht nutzen für:**
- Sensible Produktionsdaten
- Öffentliche APIs ohne Authentifizierung
- High-Security-Anforderungen

✅ **Best Practices für Production-Ready:**
- Hinzufügen von `python-dotenv` für Secrets-Management
- Aktivieren von CORS mit `python-multipart`
- Implementieren Sie Rate Limiting
- Konfigurieren Sie TLS/HTTPS
- Nutzen Sie Production-ASGI-Server (Gunicorn, Uvicorn)
- Implementieren Sie Comprehensive Logging
- Schreiben Sie Integrationstests für CI/CD

---

## 📝 Lizenz

MIT License — Frei verwendbar für Lern- und Entwicklungszwecke.

---

## 👤 Kontakt & Fragen

**Autorin:** Yana Zimmer  
**Universität:** HS Coburg  
**Programm:** Wirtschaftsinformatik (2. Semester)  
**Kurs:** Angewandte Programmierung

**Fragen zum Projekt?**  
Konsultieren Sie [`work-log.md`](work-log.md) für detaillierte Erklärungen oder öffnen Sie ein Issue im GitHub-Repository.

---

**Viel Erfolg beim Lernen! 🎓✨**