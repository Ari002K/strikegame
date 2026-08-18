import json
import os
import streamlit as st
from streamlit_autorefresh import st_autorefresh

DATA_FILE = "punkte_daten.json"

def lade_daten():
    if not os.path.exists(DATA_FILE):
        return {"Bleona": 0.0, "Arion": 0.0}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"Bleona": 0.0, "Arion": 0.0}

def speichere_daten(daten):
    with open(DATA_FILE, "w") as f:
        json.dump(daten, f)

st.set_page_config(page_title="Live Punkte", page_icon="⚡")
st_autorefresh(interval=2000, key="live_update")

daten = lade_daten()

st.title("⚡ Punkte-Duell")
st.markdown("---")

col1, col2 = st.columns(2)

def update_score(name, delta):
    neuer_wert = daten[name] + delta
    
    # Check: Max -2.9 limit
    if neuer_wert < -2.9:
        st.error("Ku po do me shku")
        return

    daten[name] = round(neuer_wert, 1)
    speichere_daten(daten)
    st.rerun()

# UI für Bleona
with col1:
    st.subheader("Bleona")
    st.markdown(f"## {daten['Bleona']}")
    if st.button("➕ 0.5", key="b_plus"): update_score("Bleona", 0.5)
    if st.button("➖ 0.5", key="b_minus"): update_score("Bleona", -0.5)

# UI für Arion
with col2:
    st.subheader("Arion")
    st.markdown(f"## {daten['Arion']}")
    if st.button("➕ 0.5", key="a_plus"): update_score("Arion", 0.5)
    if st.button("➖ 0.5", key="a_minus"): update_score("Arion", -0.5)

st.markdown("---")
if st.button("🔄 Reset"):
    speichere_daten({"Bleona": 0.0, "Arion": 0.0})
    st.rerun()
