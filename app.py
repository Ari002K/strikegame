import json
import os
import streamlit as st
from streamlit_autorefresh import st_autorefresh

DATA_FILE = "punkte_daten.json"

def lade_daten():
    standard = {
        "Bleona": 0.0, 
        "Arion": 0.0,
        "reward_3": "",
        "reward_5": "",
        "reward_10": ""
    }
    if not os.path.exists(DATA_FILE):
        return standard
    try:
        with open(DATA_FILE, "r") as f:
            daten = json.load(f)
            # Fehlende Schlüssel ergänzen, falls alte Daten existieren
            for key in standard:
                if key not in daten:
                    daten[key] = standard[key]
            return daten
    except:
        return standard

def speichere_daten(daten):
    with open(DATA_FILE, "w") as f:
        json.dump(daten, f)

st.set_page_config(page_title="Live Punkte", page_icon="⚡")
st_autorefresh(interval=2000, key="live_update")

daten = lade_daten()

st.title("⚡ Bleona vs Arion")
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

# --- BELOHNUNGEN BEREICH ---
st.subheader("🎁 Belohnungen")

def update_reward(key, text):
    daten[key] = text
    speichere_daten(daten)

# Textfelder für Belohnungen
r3 = st.text_input("Bei 3 Punkten:", value=daten["reward_3"], key="input_r3")
if r3 != daten["reward_3"]:
    update_reward("reward_3", r3)

r5 = st.text_input("Bei 5 Punkten:", value=daten["reward_5"], key="input_r5")
if r5 != daten["reward_5"]:
    update_reward("reward_5", r5)

r10 = st.text_input("Bei 10 Punkten:", value=daten["reward_10"], key="input_r10")
if r10 != daten["reward_10"]:
    update_reward("reward_10", r10)

st.markdown("---")
if st.button("🔄 Alles zurücksetzen (Reset)"):
    speichere_daten({
        "Bleona": 0.0, 
        "Arion": 0.0,
        "reward_3": "",
        "reward_5": "",
        "reward_10": ""
    })
    st.rerun()
