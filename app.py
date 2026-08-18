import json
import os
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Dateipfad für den einfachen "Datenbank"-Ersatz
DATA_FILE = "punkte_daten.json"


def lade_daten():
  """Lädt die Punkte aus der JSON-Datei oder erstellt Standardwerte."""
  if not os.path.exists(DATA_FILE):
    standard_daten = {"team1": 0, "team2": 0}
    speichere_daten(standard_daten)
    return standard_daten
  try:
    with open(DATA_FILE, "r") as f:
      return json.load(f)
  except:
    return {"team1": 0, "team2": 0}


def speichere_daten(daten):
  """Speichert die Punkte in die JSON-Datei."""
  with open(DATA_FILE, "w") as f:
      json.dump(daten, f)


# --- UI SETUP ---
st.set_page_config(page_title="Live Punktestand", page_icon="⚡", layout="centered")

# Automatischer Refresh alle 2 Sekunden (damit User B sieht, was User A klickt)
st_autorefresh(interval=2000, key="live_update")

# Daten laden
daten = lade_daten()

st.title("⚡ Live Punktestand")
st.write(
    "Jeder mit diesem Link sieht die Änderungen nach maximal 2 Sekunden"
    " automatisch!"
)

st.markdown("---")

# Anzeige der Punkte in großen Spalten
col1, col2 = st.columns(2)

with col1:
  st.subheader("Team 1")
  st.markdown(
      f"<h1 style='text-align: center; color: #ff4b4b;'>{daten['team1']}</h1>",
      unsafe_allow_html=True,
  )

  # Buttons für Team 1
  if st.button("➕ Punkt für Team 1", use_container_width=True):
    daten["team1"] += 1
    speichere_daten(daten)
    st.rerun()

  if st.button("➖ Abzug Team 1", use_container_width=True):
    daten["team1"] = max(0, daten["team1"] - 1)
    speichere_daten(daten)
    st.rerun()

with col2:
  st.subheader("Team 2")
  st.markdown(
      f"<h1 style='text-align: center; color: #1c83e1;'>{daten['team2']}</h1>",
      unsafe_allow_html=True,
  )

  # Buttons für Team 2
  if st.button("➕ Punkt für Team 2", use_container_width=True):
    daten["team2"] += 1
    speichere_daten(daten)
    st.rerun()

  if st.button("➖ Abzug Team 2", use_container_width=True):
    daten["team2"] = max(0, daten["team2"] - 1)
    speichere_daten(daten)
    st.rerun()

st.markdown("---")

# Reset-Button
if st.button("🔄 Alles zurücksetzen (Reset)", use_container_width=True):
  speichere_daten({"team1": 0, "team2": 0})
  st.rerun()
