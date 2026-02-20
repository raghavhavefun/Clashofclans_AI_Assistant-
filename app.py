import streamlit as st
import requests
import subprocess
from streamlit_mic_recorder import mic_recorder
from faster_whisper import WhisperModel
from piper import PiperVoice
import tempfile
import os
import numpy as np
import io
import wave
import time
import base64
import random
import re
import uuid

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(page_title="Clash Companion AI", layout="wide")

# -------------------------------------------------
# LOAD CSS
# -------------------------------------------------

def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown('<div class="main-header">Clash Companion AI 🚀</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Strategic AI Coach (Stats + Vision + Voice)</div>', unsafe_allow_html=True)

# -------------------------------------------------
# API KEY
# -------------------------------------------------

COC_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJlYzY0Y2JjLTI4N2EtNDQ1Ny05OGM3LTMxNzlhNDZhZGI3ZCIsImlhdCI6MTc3MTU0MjUzOSwic3ViIjoiZGV2ZWxvcGVyL2U3NjIzMDFmLWU2ZTUtZmY5MS00MjUwLTBhYWY4YjAxNjcxYyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjIyMy4xODUuMzEuMTc4Il0sInR5cGUiOiJjbGllbnQifV19.f7t1BhJFKVNrZYtPSzRasbxj4JUfFbHEl5TpUnQaL7EOKVU3dhy3j5bjk3SEEF9kkdSZHQGO1piy2XoNdva4pQ"

# -------------------------------------------------
# FILE PATHS
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IDLE_PATH = os.path.join(BASE_DIR, "avatar.png")
TALKING_PATH = os.path.join(BASE_DIR, "avatartalking.gif")
PIPER_MODEL_PATH = os.path.join(BASE_DIR, "en_US-lessac-medium.onnx")

# -------------------------------------------------
# SESSION DEFAULTS
# -------------------------------------------------

defaults = {
    "player_data": None,
    "chat_history": [],
    "voice_text": "",
    "current_audio": None,
    "avatar_state": "idle",
    "audio_start_time": None,
    "audio_duration": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------------------------------------
# LOAD MODELS
# -------------------------------------------------

if "whisper_model" not in st.session_state:
    st.session_state.whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")

if "piper_voice" not in st.session_state:
    st.session_state.piper_voice = PiperVoice.load(PIPER_MODEL_PATH)

# -------------------------------------------------
# OLLAMA
# -------------------------------------------------

def ask_mistral(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def ask_llava(prompt, image_path):
    result = subprocess.run(
        ["ollama", "run", "llava", image_path],
        input=prompt,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

# -------------------------------------------------
# TTS
# -------------------------------------------------

def generate_audio_bytes(text):
    audio_chunks = []
    for chunk in st.session_state.piper_voice.synthesize(text):
        audio_chunks.append(chunk.audio_float_array)

    if not audio_chunks:
        return None, 0

    full_audio = np.concatenate(audio_chunks)
    audio_int16 = (full_audio * 32767).astype(np.int16)

    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(22050)
        wf.writeframes(audio_int16.tobytes())

    duration = len(audio_int16) / 22050
    buffer.seek(0)
    return buffer, duration

# -------------------------------------------------
# LOAD PLAYER
# -------------------------------------------------

st.markdown("## 🔎 Load Player")
player_tag = st.text_input("Enter Player Tag (without #):")

if st.button("Analyze Player") and player_tag:
    headers = {"Authorization": f"Bearer {COC_API_KEY}"}
    url = f"https://api.clashofclans.com/v1/players/%23{player_tag}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        st.session_state.player_data = {
            "name": data.get("name"),
            "town_hall": data.get("townHallLevel"),
            "trophies": data.get("trophies"),
            "war_stars": data.get("warStars"),
        }
        st.session_state.chat_history = []
        st.success("Player Loaded Successfully!")
    else:
        st.error("Invalid player tag or API issue.")

# -------------------------------------------------
# MAIN SYSTEM
# -------------------------------------------------

if st.session_state.player_data:

    pdata = st.session_state.player_data

    # ---------------- PLAYER OVERVIEW ----------------

    st.markdown("## 🏰 Player Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Name", pdata["name"])
    c2.metric("Town Hall", pdata["town_hall"])
    c3.metric("Trophies", pdata["trophies"])
    c4.metric("War Stars", pdata["war_stars"])

    st.markdown("---")

    # ---------------- IMAGE UPLOAD ----------------

    st.markdown("## 📸 Upload Base Screenshot (Optional)")
    uploaded_image = st.file_uploader("Upload base screenshot", type=["png","jpg","jpeg"])

    image_analysis = ""

    if uploaded_image:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(uploaded_image.read())
            temp_path = tmp.name

        vision_prompt = """
Identify base type (War / Trophy / Farming / Hybrid).
Give short weakness summary.
"""

        image_analysis = ask_llava(vision_prompt, temp_path)

        rating_prompt = f"""
Based on this:

{image_analysis}

Return ONLY:
Attack X/10
Defense X/10
Creativity X/10
Overall X/10
"""

        rating_text = ask_mistral(rating_prompt)
        os.remove(temp_path)

        scores = re.findall(r'(\d+)/10', rating_text)

        if len(scores) >= 4:
            attack, defense, creativity, overall = [int(x) for x in scores[:4]]
        else:
            attack = defense = creativity = overall = 7

        st.markdown("### 🧠 Base Rating")
        st.markdown("**Attack**")
        st.progress(attack/10)
        st.markdown("**Defense**")
        st.progress(defense/10)
        st.markdown("**Creativity**")
        st.progress(creativity/10)
        st.markdown("**Overall**")
        st.progress(overall/10)

        st.success("Base analysis complete.")

    st.markdown("---")

    # ---------------- QUESTION SECTION ----------------

    st.markdown("## 💬 Ask Your Clash Coach")
    mode = st.radio("Choose Input Mode:", ["Type", "Voice"])
    reply = None

    def build_prompt(q):
        return f"""
Answer SHORT.
Max 5 bullets.
Direct.
Tactical.
Human tone.

Town Hall: {pdata['town_hall']}
Question: {q}
"""

    if mode == "Type":
        user_question = st.text_input("Type question:")
        if st.button("Ask Coach") and user_question:
            reply = ask_mistral(build_prompt(user_question))
            st.session_state.chat_history.append(("You", user_question))
            st.session_state.chat_history.append(("Coach", reply))

    if mode == "Voice":

        audio = mic_recorder(start_prompt="Start Recording",
                             stop_prompt="Stop Recording",
                             key="recorder")

        if audio and audio["bytes"]:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio["bytes"])
                temp_path = tmp.name

            segments, _ = st.session_state.whisper_model.transcribe(temp_path)
            detected_text = "".join(segment.text for segment in segments)
            st.session_state.voice_text = detected_text.strip()
            os.remove(temp_path)

        preview = st.text_area("Preview:", value=st.session_state.voice_text)

        if st.button("Send to Coach") and preview:
            reply = ask_mistral(build_prompt(preview))
            st.session_state.chat_history.append(("You", preview))
            st.session_state.chat_history.append(("Coach", reply))
            st.session_state.voice_text = ""

    # -------------------------------------------------
    # AUDIO + AVATAR (RESTORED)
    # -------------------------------------------------

    if reply:
        audio_buffer, duration = generate_audio_bytes(reply)
        st.session_state.current_audio = audio_buffer
        st.session_state.audio_duration = duration
        st.session_state.audio_start_time = time.time()
        st.session_state.avatar_state = "talking"

    if st.session_state.current_audio:

        elapsed = time.time() - st.session_state.audio_start_time

        if elapsed >= st.session_state.audio_duration:
            st.session_state.current_audio = None
            st.session_state.avatar_state = "idle"
            st.rerun()

        st.markdown("### 🤖 Coach Speaking")

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            if st.session_state.avatar_state == "talking":
                with open(TALKING_PATH, "rb") as f:
                    gif_base64 = base64.b64encode(f.read()).decode()
                st.markdown(
                    f'<div class="avatar-container"><img src="data:image/gif;base64,{gif_base64}" width="260"></div>',
                    unsafe_allow_html=True
                )
            else:
                st.image(IDLE_PATH, width=260)

        st.audio(st.session_state.current_audio, format="audio/wav", autoplay=True)

        if st.button("🔇 Stop AI Voice"):
            st.session_state.current_audio = None
            st.session_state.avatar_state = "idle"
            st.rerun()

    # ---------------- CHAT DISPLAY ----------------

    st.markdown("---")
    st.markdown("## 💬 Conversation")

    for role, message in st.session_state.chat_history:
        if role == "You":
            st.markdown(f'<div class="user-bubble"><b>You:</b> {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="coach-bubble"><b>Coach:</b> {message}</div>', unsafe_allow_html=True)

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.current_audio = None
        st.session_state.avatar_state = "idle"
        st.rerun()
