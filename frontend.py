# streamlit installieren
# streamlit app "Hello World" erstellen und testen
# "say no" - app als ersten Teste rstellen
# API: https://github.com/hotheadhacker/no-as-a-service
# API Endpoint: https://naas.isalman.dev/no
# button in streamlit der bei klick eine anfrage an die API endpoint sendet und die Antwort anzeigt

import requests
import streamlit as st

URL = "https://naas.isalman.dev/no"                         # Initiativ den API Endpoint angeben 
def request_no():                                           # request_no sendet get Anfrage mit requests.get(URL) an die URL  
    response = requests.get(URL)                            # und bekommt eine response zurück         
    response_json = response.json()                         # response.json() konvertiert die response in ein JSON-Format,
    return response_json["reason"]                          # Die Funktion gibt anschließend response_json["reason"] zurück.
 
# Initialisierung von session state für die beiden Texte, damit sie auch ohne Klick auf die Buttons schon einen 
# Wert haben und angezeigt werden können.

if "text1" not in st.session_state:
    st.session_state["text1"] = request_no()

if "text" not in st.session_state:
    st.session_state["text"] = request_no()


if st.button("Neuer Text 1"):
    st.session_state["text1"] = request_no()

st.write(st.session_state["text1"])
   

if st.button("Neuer Text"):
    st.session_state["text"] = request_no()

st.write(st.session_state["text"])

with st.expander("session state"):
    st.write(st.session_state)


# Bau eiens Textfeldes, man kann Namen eingeben und er wird dann angezeigt. 
# st.text_input() benötigt ein Label, das über dem Textfeld angezeigt wird (hier der Wert in der Klammer) 
# ohne das "Name" in der Klammer würde es nur Error ausgeben.


name = st.text_input("Name")
st.write(name)


### Notizen-API ###
NOTES_API = "http://127.0.0.1:8000"                         # URL des meiner FastApi App


def fetch_notes():                                          # abrufen der vorhandenen Notizen durch eine GET-Anfrage an den Endpoint "/notes" des Backends.
    response = requests.get(f"{NOTES_API}/notes")
    response.raise_for_status()
    return response.json()


def create_note(title, content, category, tags):            # hierdurch kann man dann eine neue Liste machen
    return requests.post(
        f"{NOTES_API}/notes",
        json={"title": title, "content": content, "category": category, "tags": tags},
    )


st.header("Notizen")

if st.button("Alle Notizen anzeigen"):                      # bei Klick wird eine neue Liste geladen
    try:
        st.session_state["notes_list"] = fetch_notes()
    except requests.exceptions.ConnectionError:
        st.error("Backend nicht erreichbar - läuft uvicorn auf Port 8000?")

if st.button("Neue Notiz erstellen"):                       # Formular anzeigen wenn man klickt
    st.session_state["show_form"] = True

# Liste soll durch den nächsten Block überhaupt mal angezeigt werden.
if "notes_list" in st.session_state:
    for note in st.session_state["notes_list"]:
        with st.expander(note["title"]):
            st.write(f"**Inhalt:** {note['content']}")
            st.write(f"**Kategorie:** {note['category']}")
            tag_str = ", ".join(note["tags"]) if note["tags"] else "—"
            st.write(f"**Tags:** {tag_str}")
            st.caption(f"id={note['id']} · {note['created_at']}")

# Der nächste Block sorgt dafür, dass das Formular zum Erstellen einer neuen Notiz angezeigt wird, wenn der entsprechende Button geklickt wurde.
if st.session_state.get("show_form"):
    with st.form("new_note_form", clear_on_submit=True):
        new_title = st.text_input("Titel")
        new_content = st.text_area("Inhalt")
        new_category = st.text_input("Kategorie")
        new_tags = st.text_input("Tags (kommagetrennt, optional)")
        submitted = st.form_submit_button("Speichern")

    if submitted:
        tags_list = [t.strip() for t in new_tags.split(",") if t.strip()]
        try:
            response = create_note(new_title, new_content, new_category, tags_list)
            if response.status_code == 201:
                st.success(f"Notiz angelegt (id={response.json()['id']})")
            else:
                detail = response.json().get("detail", response.text)
                st.error(f"Fehler {response.status_code}: {detail}")
        except requests.exceptions.ConnectionError:
            st.error("Backend nicht erreichbar - läuft uvicorn auf Port 8000?")
