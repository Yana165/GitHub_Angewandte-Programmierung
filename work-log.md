# Arbeitslog

**Studentin:** Yana Zimmer

**Anleitung:** Ein Log pro Kurstag ausfüllen. Inhalte: Kurssitzungen + Aufgaben

## Woche 1

### Tag 1 — Setup & Erste API

#### 1. ✅ Was habe ich erreicht?

Heute habe ich meine vollständige Entwicklungsumgebung eingerichtet, indem ich Git, VS Code und den `uv`-Paketmanager installiert habe. Ich habe mein erstes FastAPI-Projekt mit `uv init` und `uv add fastapi` erstellt und eine funktionierende API-Anwendung in `main.py` mit drei während des Kurses entwickelten Endpunkten (`GET /`, `GET /status`, `GET /about`) gebaut. Ich habe die automatische interaktive Dokumentation von FastAPI unter `/docs` erforscht und alle Endpunkte erfolgreich getestet. Für die Hausaufgaben habe ich drei zusätzliche Endpunkte implementiert: `GET /square/{number}` zum Berechnen von Quadraten mit formatierten Antwortzeichenketten, `GET /student` zur Rückgabe meiner persönlichen Informationen (Name: Yana Zimmer, Semester: 2, Universität: HS Coburg) und `GET /double/{number}` zum Verdoppeln von Werten. Ich habe überprüft, dass alle sechs Endpunkte korrekte JSON-Antworten zurückgeben und auf `http://127.0.0.1:8000` korrekt funktionieren.

---

#### 2. 🚧 Welche Herausforderungen bin ich aufgetroffen?

Meine Hauptschwierigkeit war, den konzeptionellen Unterschied zwischen einem API-Endpunkt und einer normalen Python-Funktion zu verstehen, ich kämpfte zunächst damit zu verstehen, warum `@app.get("/")` eine Funktion über eine Browser-URL abrufbar macht. Ich bin auch auf ein frustrierendes technisches Problem gestoßen: Nach der Installation von FastAPI mit `uv add fastapi` ist der Befehl `uv run fastapi dev` mit „No such file or directory" fehlgeschlagen, weil die Standard-CLI-Tools fehlten (die `fastapi[standard]`-Variante war erforderlich, nicht nur `fastapi`). Zusätzlich bin ich auf einen Port-Konflikt gestoßen, als Port 8000 bereits von einem anderen Prozess verwendet wurde, was den Start des Servers verhinderte und eine verwirrende Fehlermeldung ohne klare Anleitung zur Behebung gab. Ich finde mich gerade im Thema Programmieren erst ein und bin noch Beginner.

---

#### 3. 💡 Wie habe ich sie überwunden?

Um das API-Konzept zu verstehen, nutzte ich die Restaurant-Analogie aus den Folien (Kunde → Kellner → Küche) und testete die Endpunkte wiederholt direkt im Browser und in `/docs`, bis der Request-Response-Fluss intuitiv wurde. Bei dem Installationsproblem las ich die Fehlerausgabe sorgfältig, die die Installation von `fastapi[standard]` vorschlug, führte `uv add "fastapi[standard]"` aus, und dann startete der Dev-Server erfolgreich. Beim Port-Konflikt startete ich meine Terminal-Sitzung neu, um hängende Prozesse zu löschen, nutzte dann `pkill`, um Port 8000 freizugeben, bevor ich den Server neu startete. Aus diesen Problemen lernte ich, Fehlermeldungen sorgfältig zu lesen und die Paketinstallation vollständig zu überprüfen, bevor ich von einem abgeschlossenen Setup ausgehe. Das ist super wichtig!

---

### Tag 2 — Python-Grundlagen & Notizen-Management-API

#### 1. ✅ Was habe ich erreicht?

Ich habe meine Python-Grundlagen vertieft, indem ich Variablen, Datentypen (str, int, float, bool, list, dict), f-Zeichenketten, Typ-Hinweise und Funktionsdefinitionen mit Rückgabetypen praktizierte. Ich studierte HTTP-Methoden (`GET` vs `POST`) und JSON als Standard-API-Datenformat. Die Hauptleistung war der Aufbau einer Notizen-API mit drei Kern-Endpunkten: `POST /notes` zum Erstellen von Notizen, `GET /notes` zum Auflisten aller Notizen und `GET /notes/{note_id}` zum Abrufen spezifischer Notizen. Ich definierte Pydantic-Modelle (`NoteCreate` für Eingaben, `Note` für Ausgaben) mit automatischer Validierung. Ich implementierte dateibasierte Persistierung mit `json.load` und `json.dump`, damit Notizen Server-Neustarts überdauern — die Funktionen `load_notes()` und `save_notes()` lesen von und schreiben in `data/notes.json`. Für die Hausaufgaben erweiterte ich das Datenmodell um ein `category`-Feld, fügte einen `GET /notes/category/{category}`-Filter-Endpunkt hinzu und baute einen `GET /notes/stats`-Endpunkt, der Gesamtzahl und kategoriespezifische Statistiken zurückgibt.

---

#### 2. 🚧 Welche Herausforderungen bin ich aufgetroffen?

Die Unterscheidung zwischen `POST` und `GET` war sehr herausfordernd: Ich verstand zunächst niicht vollständig, warum `POST` einen Request-Body erfordert, während `GET`-Parameter in die URL gehen. Die Implementierung der Datei-Persistierung war technisch schwierig auch, ich kämpfte mit der Funktion `load_notes()`, weil ich unsicher war, wie ich JSON-Daten zurück in Pydantic-`Note`-Objekte konvertiere und wie ich einen ordnungsgemäßen ID-Zähler über Server-Neustarts hinweg pflege. Ich machte auch einen krassen Fehler, indem ich vergaß, `save_notes()` nach dem `create_note()`-Endpunkt aufzurufen, was dazu führte, dass alle neu erstellten Notizen beim Server-Stopp verschwanden. Zusätzlich definierte ich zunächst den `NOTES_FILE`-Pfad nach den Funktionen, die ihn verwendeten, was einen `NameError` verursachte.

---

#### 3. 💡 Wie habe ich sie überwunden?

Ich überwand die `POST`/`GET`-Verwirrung, indem ich Notizen via `/docs` erstellte und die Request-Body-Struktur beobachtete, diese dann mit einfachen URL-basierten `GET`-Anfragen verglich, bis das Muster klar wurde. Darauf bin ich gekommen, da ich den Copilot gefragt habe. Für die Datei-Persistierung habe ich die Folie-Beispiele erneut durchgelesen, die `Note(**note)` zur Deserialisierung von JSON zurück in Pydantic-Objekte zeigten, und `max(note.id for note in notes_db) + 1` für die ID-Zähler-Logik. Ich behob den fehlenden `save_notes()`-Aufruf, indem ich ihn unmittelbar nach `notes_db.append(new_note)` hinzufügte und die Persistierung überprüfte, indem ich den Server stoppte und neu startete. Um den `NameError` zu beheben, reorganisierte ich meinen Code, um alle Dateipfade und Hilfsfunktionen vor den Endpunkt-Definitionen zu definieren. Ich lernte, dass Code-Reihenfolge in Python zählt und dass Persistierung explizite Speicheroperationen nach jeder ändernden Aktion erfordert. Auf diesen Tag war ich stolz, da ich die ersten Erfolge jetzt schon sehen konnte, obwohl es auch anstrengend ist. Es beginnt echt Spaß zu machen!

---

### Tag 3 — REST-API-Design & Vollständige CRUD-Operationen

#### 1. ✅ Was habe ich erreicht?

Ich lernte REST-API-Designprinzipien einschließlich ressourcen-basierter URLs (Substantive, keine Verben), ordnungsgemäße Verwendung von HTTP-Methoden (`GET`, `POST`, `PUT`, `DELETE`), und zustandslose Architektur. Ich unterschied zwischen Pfad-Parametern (zur Identifikation: `/notes/{id}`) und Query-Parametern (zum Filtern: `/notes?category=work`). Ich erweiterte meine Notizen-API zu v2.0, indem ich vollständige CRUD-Operationen hinzufügte: `PUT /notes/{note_id}` für vollständige Updates und `DELETE /notes/{note_id}` mit Status-Code 204. Ich implementierte Query-Parameter-Filterung auf `GET /notes` mit Unterstützung für Kategorie, Suche (case-insensitive in Titel und Inhalt) und Tag-Filter, die mit AND-Logik kombiniert werden können. Ich fügte array-basierte Tags zum Datenmodell hinzu, baute Ressourcen-Beziehungs-Endpunkte (`GET /tags` für eindeutige Tags, `GET /tags/{tag_name}/notes` für tag-basierte Abfrage), und erkundete die Auswirkungen der Endpunkt-Reihenfolge durch praktische Übung. Für die Hausaufgaben kombinierte ich mehrere Filter, baute einen Statistik-Endpunkt mit Top-Tags und eindeutiger Tag-Anzahl, fügte `/categories` und `/categories/{category}/notes`-Ressourcen-Endpunkte hinzu, implementierte `PATCH` für teilweise Updates, fügte datumsbasiertes Filtern mit ISO-Zeichenkettenvergleichen hinzu, und migrierte von JSON-Dateispeicherung zu einer SQLite-Datenbank unter Verwendung von SQLModel mit Many-to-Many-Beziehungen zwischen Note und Tag. Dieser Tag war bisher der Tag, an dem wir am meisten Stoff gemacht haben und neues gelernt haben. Außerdem habe ich heute gelernt wie wichtig es ist wirklich zu pushen ins Repository, das ist ein wirklicher gamechanger!


---

#### 2. 🚧 Welche Herausforderungen bin ich aufgetroffen?

REST-API-URL-Design war zunächst kontraintuitiv, mein Instinkt war, verb-basierte Pfade wie `/getNotes` oder `/deleteNote` zu verwenden, und das Wechseln zu nur Substantiv-Ressourcen (`/notes`, `/notes/{id}`) erforderte bewusste Anstrengung. Der Unterschied zwischen `PUT` und `PATCH` war wichtig: Ich implementierte zunächst `PUT`, das alle Felder erforderte, kämpfte dann zu verstehen, warum `PATCH` teilweise Updates ohne Auswirkung auf unveränderte Felder ermöglichen sollte. Die Filterlogik mit mehreren kombinierten Bedingungen wurde komplex, besonders als ich `if`-Anweisungen mit `continue` verketten musste, um AND-Logik über Kategorie-, Such- und Tag-Filter zu implementieren. Die Datenbankmigrationen (Aufgabe 6) war die größte Herausforderung — SQLModel einrichten, Many-to-Many-Beziehungen mit impliziten Link-Tabellen verstehen, die `SessionDep`-Abhängigkeit erstellen und alle dateibasierten Operationen in Datenbankabfragen mit `select()`, `session.exec()` und `session.commit()` konvertieren erforderte erhebliche mentale Umstrukturierung. Ich kämpfte auch mit Tag-Deduplizierung und case-insensitiver Suche beim Migrieren der Tag-Logik zur Datenbank-Schicht.

---

#### 3. 💡 Wie habe ich sie überwunden?

Um REST-Konventionen zu verinnerlichen, überprüfte ich die Folie „Good vs Bad URL Design" wiederholt, habe den Copiloten nochmal gefragt und benannte alle Endpunkte um, um dem `/resources`- und `/resources/{id}`-Muster zu folgen. Für `PUT` vs `PATCH` erstellte ich ein separates `NoteUpdate`-Modell mit `Optional`-Feldern und schrieb explizite Logik, die nur Felder überschreibt, die nicht `None` sind, was die Unterscheidung klärte. Für kombinierte Filterung zeichnete ich ein Ablaufdiagramm auf Papier, das zeigte, wie jede Filterbedingung Notizen, die nicht passen, überspringen sollte, und übersetzte diese Logik dann in Code mit verschachtelten `if`-Anweisungen. Die SQLModel-Migration war die zeitaufwendigste — ich arbeitete sie Schritt für Schritt: zuerst `sqlmodel` installieren, dann `Note`- und `Tag`-Tabellen mit `Relationship(back_populates=...)` definieren, das Engine und `get_session()` Setup durchführen, und erst dann Endpunkt für Endpunkt umschreiben (mit `POST` beginnend, dann `GET`-Liste, dann `GET` nach ID, usw.). Ich nutzte den VS Code SQLite-Viewer, um die generierte `notes.db`-Datei zu inspizieren und zu überprüfen, dass die Link-Tabelle korrekt erstellt wurde. Für Tag-Deduplizierung implementierte ich ein „get or create"-Muster mit `select(Tag).where(Tag.name == tag_name_lower)`, bevor Tags mit Notizen verknüpft wurden. Im Großen und Ganzen kann ich jetzt schon sagen, dass ich dadurch jetzt schon viel gelernt habe für meine berufliche Zukunft, weil man diese Funktion sehr häufig brauchen wird. 

---

## Woche 2

### Tag 4 — POST-Endpunkte & Daten erstellen

#### 1. ✅ Was habe ich erreicht?

Ich konzentrierte mich auf POST-Anfragen und Pydantic-Datenvalidierung, lernte die strukturellen Unterschiede zwischen GET (Abruf, kein Body) und POST (Erstellung, Request-Body). Ich baute eine Kurs-Katalog-API mit `POST /courses`, das Status 201 zurückgibt, implementierte Pydantic-Modelle (`CourseCreate` für Eingabe ohne ID, `Course` für Ausgabe mit ID) und fügte Duplikat-Erkennung mit case-insensitiver Code-Vergleich hinzu, die 409-Konflikt zurückgibt. Ich richtete Datei-Persistierung für Kurse mit dem gleichen `load_courses()` / `save_courses()`-Muster von Tag 2 ein. Ich lernte über `**course.dict()` zum Auspacken von Pydantic-Modellen in Konstruktoren. Ich studierte dann pytest-Test-Ansätze: externes Testen mit der `requests`-Bibliothek (erfordert laufenden Server) und internes Testen mit FastAPI's `TestClient` (kein Server nötig). Ich schrieb Tests nach dem Arrange-Act-Assert-Muster, ab deckend Wurzel-Endpunkte, CRUD-Operationen, 404-Fehler und Query-Parameter-Filterung. Für die Hausaufgaben schrieb ich eine umfassende Test-Suite für meine Notizen-API, die alle Features von Tag 2 und 3 abdeckt.

---

#### 2. 🚧 Welche Herausforderungen bin ich aufgetroffen?

Meine ersten pytest-Tests zu schreiben war wirklich schwierig. Ich verwechselte zunächst die zwei Test-Ansätze und versuchte, `TestClient` zu verwenden, während der Server lief, was zu unerwartetem Verhalten führte. Das Arrange-Act-Assert-Muster zu verstehen dauerte Zeit, ich vergaß kontinuierlich, Assertions zu schreiben, die tatsächlich den Antwortinhalt überprüfen, anstatt nur den Status-Code. Beim Testen von Fehlerfällen war ich unsicher, wie ich auf die `detail`-Nachricht von `HTTPException`-Antworten assert'e. Ich entdeckte auch, dass meine Tests voneinander abhängig waren, weil sie alle auf der gleichen `notes.json`-Datei operierten, was zu Fehlern bei Ausführung in verschiedenen Reihenfolgen führte. Zusätzlich fand ich es verwirrend, dass `requests` eine vollständige URL benötigt (`http://127.0.0.1:8000/notes`), während `TestClient` nur den Pfad benötigt (`/notes`).

---

#### 3. 💡 Wie habe ich sie überwunden?

Ich habe mit einem Kommilitonen viel gemeinsam an diesen Aufgaben gearbeitet. Wir haben uns gegenseitig unterstützt. Ich klärte dabei die Test-Ansätze, indem ich beide nebeneinander lief: Ich startete den Server in einem Terminal und führte `requests`-basierte Tests in einem anderen aus, stoppte dann den Server und führte `TestClient`-basierte Tests aus, um den Unterschied zu sehen. Um Arrange-Act-Assert zu beherrschen, zwang ich mich, mindestens drei Assertions pro Test zu schreiben: Status-Code, Antwortstruktur (Schlüssel-Existenz) und Antwort-Wert-Korrektheit. Zum Testen von Fehlermeldungen inspizierte ich die JSON-Struktur von 404-Antworten in `/docs` und schrieb dann Assertions wie `assert "not found" in response.json()["detail"].lower()`. Um Test-Isolation zu lösen, fügte ich Setup/Teardown-Logik hinzu, die die `notes.json`-Datei vor kritischen Tests bereinigt und sicherstellt, dass jeder Test von einem bekannten Zustand startet. Ich dokumentierte den URL-Unterschied in Kommentaren in meinen Test-Dateien, um mich selbst zu erinnern, welchen Ansatz ich verwendete. Heute habe ich vor Allem gelernt, dass man zu zweit so viel mehr lernen kann und auch sieht wie eine andere Person an Probleme rangeht. Das hat mir immens geholfen und wir haben uns entschieden öfters eine gemeinsame Lerngruppe zu machen.

---

### Tag 5 — Pydantic-Datenvalidierung Tieftauch

#### 1. ✅ Was habe ich erreicht?

Ich lernte, warum allein Typ-Validierung unzureichend ist und wie man APIs ablehnt, die schlechte Daten an der Grenze mit Pydantic akzeptieren. Ich wendete `Field(...)`-Einschränkungen an, einschließlich `min_length`, `max_length`, `pattern` (regex), `ge`/`le` für numerische Bereiche und `default_factory=list` für veränderliche Defaults. Ich verschärfte das `NoteCreate`-Modell mit Regeln wie `title: str = Field(min_length=3, max_length=100)` und `category: str = Field(pattern=r"^[a-z]+")`. Ich schrieb benutzerdefinierte `@field_validator`-Methoden für Normalisierung (Leerzeichen trimmen, Kleinschreibung) und Validierung (Kategorie muss in erlaubtem Satz sein, Tags müssen dedupliziert und kleingeschrieben werden). Ich implementierte einen `@model_validator(mode="after")` für Quer-Feld-Regeln (z.B. Arbeitsnotizen müssen das "work"-Tag enthalten). Ich konfigurierte globales Modell-Verhalten mit `ConfigDict(str_strip_whitespace=True, extra="forbid")`, um Tippfehler zu erfassen und Zeichenketten automatisch zu bereinigen. Ich erkundete integrierte Typen wie `EmailStr` und `HttpUrl`. Für die Hausaufgaben verhärtete ich `NoteCreate`, `NoteUpdate` und das `Tag`-SQLModel mit umfassenden Einschränkungen und Validierern und erstellte `test_validation.py` mit 8+ Tests, die 422-Antworten für ungültige Eingaben überprüfen.
Das Projekt wird immer vielseitiger und ich fühle mich immer sicherer im coden! Es macht wirklich spaß. 
---

#### 2. 🚧 Welche Herausforderungen bin ich aufgetroffen?

Der häufigste und stillste Bug, auf den ich stieß, war zu vergessen, den modifizierten Wert in `@field_validator`-Methoden zu `return`, ich schrieb `value.strip()` ohne es zu retournieren, was die Daten unverändert ohne Fehler ließ. `mode="before"` versus `mode="after"` in Validatoren zu verstehen war konzeptionell schwierig; ich nutzte zunächst den falschen Modus und versuchte, bereits-validierte Felder vor der Typ-Coercion zu aktualisieren. Den Tag-Validator zu schreiben war komplex, weil er durch eine Liste iterieren, jedes Element bereinigen, deduplizieren mit einem `set` und leere Zeichenketten ablehnen musste, alles in einer einzigen Validator-Funktion. Der `@model_validator`-Dekorator war verwirrend, weil er auf `self` (das gesamte Modell) operiert anstatt auf einem einzelnen Feldwert, und ich versuchte zunächst, Quer-Feld-Regeln mit `@field_validator` zu implementieren, was mehrere Felder nicht zugreifen kann. Für `NoteUpdate` kämpfte ich darum, „optional aber validiert, wenn vorhanden" auszudrücken — ich schrieb kontinuierlich Felder, die entweder zu streng (erforderlich) oder zu locker (keine Validierung) waren.

---

#### 3. 💡 Wie habe ich sie überwunden?

Wir arbeiten weiterhin viel gemeinsam in der Lerngruppe und pushen uns gegenseitig. Hierbei sind wir folgendermaßen vorgegangen: Um das fehlende Return-Problem zu beheben, adoptierte ich eine strenge Regel: jede Validator-Funktion muss mit `return value` oder `return self` enden, und ich fügte pylint-Stil-Kommentare hinzu, um mich selbst zu erinnern. Für `mode="before"` vs `mode="after"` las ich die Pydantic-Dokumentations-Beispiele sorgfältig und realisierte, dass `mode="before"` ungefilterte Eingabe sieht (nützlich für Typ-Konvertierung wie das Aufteilen von kommaseparierten Zeichenketten), während `mode="after"` coerced Modell-Felder sieht (nützlich für Geschäftslogik). Ich implementierte den Tag-Validator Schritt für Schritt: zuerst eine Schleife, die trimmt und Kleinschreibung durchführt, dann ein `set` für Deduplizierung, dann ein `if not t`-Check für leere Ablehnung, teste jeden Schritt mit Print-Debug, bevor ich finalisierte. Für `@model_validator` studierte ich das Folie-Beispiel, das `def work_notes_need_work_tag(self) -> Self` zeigte und verstand, dass `self.category` und `self.tags` bereits-validierte Felder sind, die nach allen Feld-Validatoren verfügbar sind. Für `NoteUpdate` nutzte ich das Muster `title: str | None = Field(default=None, min_length=3, max_length=100)`, das Einschränkungen nur anwendet, wenn das Feld bereitgestellt ist, mit `None` signalisiert „keine Änderung". Wir mussten wirklich lange an diesen Aufgaben arbeiten und haben dabei unter anderen auch den Copilot verwendet um uns Erklärungen zwischendurch zu geben, dies half extrem um auch alle Codes wirklich zu verstehen. 

---

## Woche 3

### Tag 6 — Testen und Decorators

#### 1. ✅ Was habe ich erreicht?

Ich lernte Python-Decorators als Mechanismus zur Trennung von Programm-Logik von administrativen Aufgaben und verstand, wie FastAPI selbst Decorators (`@app.get`) nutzt, um Endpunkt-Handler zu registrieren. Ich erstellte eine `class_based_decorator.py`-Datei zum Üben, meine eigenen Decorators zu schreiben, und nutzte die `icecream`-Bibliothek zum Debugging-Output. Der Hauptfokus lag auf der Integration und Ausführung der umfassenden Referenz-Test-Suite (`test_main.py`) aus dem Kurs-Repository gegen meine API-Implementierung. Ich lud die Test-Datei herunter, führte sie mit `uv run pytest test_main.py -v` aus und analysierte die fehlgeschlagenen Tests, um Lücken in meiner Implementierung zu identifizieren. Ich arbeitete durch mehrere Test-Kategorien einschließlich Wurzel-Endpunkte, CRUD-Operationen, Filterung, Statistiken, Ressourcen-Navigation, Validierung, Tag-Semantik, PATCH/PUT-Semantik, Grenzfälle und End-to-End-Flüsse. Für die Hausaufgaben behob ich systematisch alle fehlgeschlagenen Tests, indem ich mein API-Verhalten an die Referenz-Erwartungen ausrichtete, holte Hausaufgaben-Items nach (Datenbank-Backend-Migration, Validierungsregeln) und stellte sicher, dass mein Projekt in einem submissions-bereiten Zustand war. Es wurde also wirklich praktisch an diesem Vorlesungstag, das gefällt mir am Besten!! Zu sehen was man geschafft hat und was man noch alles erweitern könnte ist sehr cool.

---

#### 2. 🚧 Welche Herausforderungen bin ich aufgetroffen?

Das Decorator-Konzept war abstrakt und schwierig anfangs zu erfassen und zu verstehen, dass ein Decorator eine Funktion ist, die eine Funktion nimmt und eine gewrappte Funktion zurückgibt, erforderte, dass ich das Konzept mehrfach las weil ich es nicht direkt verstanden habe. Die Referenz-Test-Suite offenbarte zahlreiche Probleme, die ich mir nicht bewusst war: meine Tag-Normalisierung war case-sensitiv statt case-insensitiv, mein `DELETE`-Endpunkt gab 200 statt 204 zurück, `PATCH` mit leerem Body `{}` war fehlgeschlagen statt erfolgreich, und mein Stats-Endpunkt passte nicht zur erwarteten Antwort-Form (fehlende `top_tags`-Format oder `unique_tag_count`). Die volle Suite ausführen produzierte eine Wand von roten Fehlschlägen, die sich überwältigend anfühlte. Ich entdeckte auch, dass einige Endpunkte, die ich dachte, dass sie funktionieren (wie `/tags/{tag}/notes`, das `[]` für unbekannte Tags zurückgibt), tatsächlich 404 in meiner Implementierung zurückgaben, was gegen die Referenz-Anforderungen verstieß.

---

#### 3. 💡 Wie habe ich sie überwunden?

Für Decorators schrieb ich einen einfachen Logging-Decorator von Grund auf, der vor und nach Funktionsaufrufen ausdruckt, und wandte ihn dann auf mehrere meiner eigenen Funktionen an, bis das Wrapper-Muster intuitiv wurde. Um die Test-Suite-Fehlschläge ohne Überwältigung zu bewältigen, nutzte ich `uv run pytest test_main.py -v -k "test_name"`, um einen fehlgeschlagenen Test gleichzeitig auszuführen, behob das entsprechende Endpunkt-Verhalten und bewegte mich dann zum nächsten. Ich erstellte eine Checkliste der Fehler-Kategorien: Status-Codes (behob `DELETE`, um nichts mit 204 zurückzugeben, behob `PATCH`-leerer Body, um 200 zurückzugeben), Case-Sensitivität (fügte `.lower()` zu allen Tag- und Kategorie-Vergleichen hinzu), Antwort-Formen (spellte Stats zur exakten erwarteten JSON-Struktur aus) und fehlende Endpunkte (fügte ordnungsgemäße Handhabung für unbekannte Ressourcen hinzu, die `[]` statt 404 zurückgeben). Ich führte die volle Suite nach jeder Kategorie-Behebung aus, um Fortschritt zu messen. Dieser iterative Ansatz transformierte eine einschüchternde rote Wand in eine Reihe von lösbaren, konkreten Problemen. Heute war ich echt lange festgehangen.

---

### Tag 7 — Frontend mit Streamlit

#### 1. ✅ Was habe ich erreicht?

Ich baute meine erste Frontend-Anwendung mit Streamlit, einer Python-Bibliothek zum Erstellen von Web-GUIs ohne HTML/CSS. Ich installierte Streamlit mit `uv add streamlit`, erstellte eine „Hallo, Welt"-Streamlit-Anwendung und baute eine „Say No"-Anwendung, die Anfragen an eine externe API (`https://naas.isalman.dev/no`) sendet und Antworten zeigt, wenn auf Buttons geklickt wird. Ich lernte über Streamlits Ausführungs-Modell, Sitzungszustand-Verwaltung (`st.session_state`) zum Beibehalten von Daten zwischen Interaktionen und Input-Widgets wie `st.text_input`, `st.button` und `st.expander`. Ich erkundete `st.form` für Multi-Input-Submission. Für die Hausaufgaben baute ich eine `frontend.py`-Anwendung für meine Notizen-API mit zwei Haupt-Funktionen: (1) Anzeige aller Notizen in einer Liste mit auswählbaren Titeln, die Inhalt, Tags, Kategorie und Erstellungsdatum offenbaren; und (2) ein Erstellungsformular mit Feldern für Titel, Inhalt, Tags und Kategorie, das eine POST-Anfrage zu meinem laufenden FastAPI-Backend sendet und die Notizen-Liste aktualisiert. Ich testete den vollen Fluss, indem ich FastAPI in einem Terminal und Streamlit in einem anderen startete.

---

#### 2. 🚧 Welche Herausforderungen bin ich aufgetroffen?

Streamlits reaktives Ausführungs-Modell war vollständig verschieden vom Request-Response-API-Paradigma, an das ich gewöhnt war — das Skript läuft von oben nach unten bei jeder Interaktion neu durch, was meine API-Anfragen wiederholt auslöste, bis ich lernte, `st.session_state` zu nutzen, um Daten zu cachen. Das Verwalten von zwei simultanen Prozessen (FastAPI-Server auf Port 8000 und Streamlit auf Port 8501) in separaten Terminals war operationell verwirrend; ich verwechselte kontinuierlich, welches Terminal welchen Befehl benötigte und stoppte manchmal den falschen Server. Das `st.form`-Widget für Multi-Input-Submission hatte spezifische Einschränkungen — der Submit-Button muss innerhalb des Formulars sein und alle Formular-Elemente werden zusammengefasst, was Experimentieren erforderte, um es richtig zu machen. Ich kämpfte auch damit, die Tags-Liste schön in der UI anzuzeigen, weil Streamlits Standard-Rendering von Python-Listen nicht benutzerfreundlich ist. Ein wiederkehrendes Problem war, dass neu erstellte Notizen nicht unmittelbar in der Liste nach Formular-Submission erschienen, weil ich vergaß, einen Neustart auszulösen oder den Sitzungszustand-Cache zu aktualisieren.

---

#### 3. 💡 Wie habe ich sie überwunden?

Um Streamlits Ausführungs-Modell zu verstehen, fügte ich `print()`-Anweisungen durchgehend in mein Skript ein und beobachtete die Terminal-Ausgabe, während ich auf Buttons klickte, was das von-oben-nach-unten-Neustart-Verhalten sichtbar und vorhersehbar machte. Ich strukturierte dann meinen Code so, dass er `st.session_state` vor API-Aufrufen überprüft, using Muster wie `if 'notes' not in st.session_state: st.session_state['notes'] = fetch_notes()`. Zum Verwalten von zwei Terminals bezeichnete ich jedes Terminal-Fenster explizit („Backend - FastAPI" und „Frontend - Streamlit") und erstellte ein kleines Start-Skript, das beide Befehle dokumentiert. Ich studierte die `st.form`-Dokumentations-Beispiel und baute mein Erstellungsformular, indem ich die exakte Struktur kopierte: öffne mit `with st.form("create_note"):`, positioniere Input-Felder innen, ende mit `submitted = st.form_submit_button()` und führe die POST-Anfrage nur aus, wenn `submitted` wahr ist. Für Tag-Anzeige verbinde ich die Liste mit einer kommaseparierten Zeichenkette mit `", ".join(note["tags"])`. Um sicherzustellen, dass neue Notizen unmittelbar nach Erstellung erscheinen, aktualisierte ich `st.session_state['notes']` mit der Antwort der POST-Anfrage und rief `st.rerun()` auf, um die Seitenzustand zu aktualisieren.
Insgesamt bin ich sehr zufrieden und freue mich auf das weitere Programmieren, und bin gespannt was ich noch so alles lernen kann!!

---

# 🎉 Glückwunsch! Du hast es geschafft! 🎓✨
