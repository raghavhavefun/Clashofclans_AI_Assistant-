🚀 Clash Companion AI
AI-Powered Strategic Assistant for Clash of Clans
📌 Project Overview

Clash Companion AI is a local AI-powered assistant built specifically for Clash of Clans players.

It combines:

🔎 Clash of Clans Official API integration

🧠 Local Large Language Model (LLM) via Ollama

👁️ Vision Model (LLaVA) for base screenshot analysis

🎙️ Offline Voice Assistant (Whisper + Piper TTS)

🤖 Animated AI Avatar

📊 Tactical base rating system

The assistant can:

Analyze player stats

Evaluate base screenshots

Suggest attack strategies

Generate army compositions

Speak responses using an AI avatar

Work fully offline (except CoC API)

This project is a working prototype demonstrating AI + gaming overlay intelligence.

🧠 What This Project Demonstrates

This repository shows:

How AI can analyze real gameplay data

How a Vision Language Model (VLM) can read screenshots

How to build an offline AI assistant

How to integrate speech-to-text and text-to-speech

How to connect gaming APIs to local AI models

This is a proof-of-concept for larger AI gaming systems.

⚙️ Full Setup Guide (Beginner Friendly)

Follow these steps carefully.

1️⃣ Install Required Software
✅ Install Python (3.10 or newer)

Download from:
https://www.python.org/downloads/

During installation:
✔ Check “Add Python to PATH”

✅ Install Ollama (for AI models)

Download from:
https://ollama.com/download

After installing, open Command Prompt and install models:

ollama pull mistral
ollama pull llava
2️⃣ Install Python Dependencies

Open Command Prompt inside project folder:

pip install streamlit
pip install requests
pip install faster-whisper
pip install piper-tts
pip install numpy
pip install soundfile
pip install streamlit-mic-recorder
3️⃣ Download Piper Voice Model

Go to:
https://huggingface.co/rhasspy/piper-voices

Download:

en_US-lessac-medium.onnx

en_US-lessac-medium.onnx.json

Place both files inside the project folder.

4️⃣ Get Clash of Clans API Access
Step 1 — Get Public IP

Go to:
https://whatismyipaddress.com/

Copy your IPv4 address.

Step 2 — Create Clash API Key

Go to:
https://developer.clashofclans.com/

Log in with Supercell ID

Create new API key

Add your public IP

Copy generated API key

Step 3 — Add API Key to Code

Open app.py

Replace:

COC_API_KEY = "your_key_here"

Paste your real API key inside quotes.

5️⃣ Run the Application

Inside project folder:

python -m streamlit run app.py

Browser will open automatically.

🧩 How It Works (System Architecture)
Step Flow:

User enters Player Tag

App fetches stats via Clash API

User uploads base screenshot

Screenshot → LLaVA Vision Model

Analysis → Mistral LLM

Tactical response generated

Piper converts response to voice

AI Avatar speaks answer

Everything runs locally except Clash API.

🎯 Key Features
🏰 Player Analysis

Fetches Town Hall

Trophies

War Stars

Profile stats

📸 Base Screenshot Analysis

Detects base type (War / Trophy / Farming)

Rates:

Attack

Defense

Creativity

Overall score

⚔ Army Suggestion

AI suggests optimized attack composition.

🎙 Voice Assistant

Whisper → Speech to text

Piper → Text to speech

Talking avatar animation

🤖 Offline AI

Runs fully on local system using Ollama.

🛠 Tech Stack

Python

Streamlit

Ollama (Mistral + LLaVA)

Faster-Whisper

Piper TTS

Clash of Clans API

Local GPU/CPU inference

🔮 Why This Project Matters

This is not just a gaming assistant.

It is a foundation for AI-powered companion systems, capable of:

Reading live screens

Understanding gameplay

Guiding users

Acting as a personalized AI friend

🌍 Bigger Vision

This project represents only 0.1% of a much larger platform:

🚀 Havfun
A free and fun space for diverse Gen Z communities to socialize, earn and entertain.

Clash Companion AI is a prototype module inside the Havfun ecosystem.

Havfun will include:

AI companion overlays

Social matchmaking

Community building

Marketplace integration

Map-based meetups

AI productivity tools

Gaming intelligence systems

🌐 Learn More About The Founder & Vision

Website:
https://havefun4u.com

LinkedIn:
https://www.linkedin.com/in/raghav-agarwal-86854521b

Instagram:
https://www.instagram.com/zenrag_?igsh=MW4xeGdpdXBtcHR1Ng==

⚠️ Disclaimer

This project is a prototype for research and educational purposes.
It is not affiliated with or endorsed by Supercell.

🧠 Future Roadmap

Android Overlay Integration

Real-time gameplay guidance

Reinforcement Learning

Live vision-based tactical arrows

Full Havfun integration

📌 Final Note

If you can run this project successfully, you have:

Integrated an official gaming API

Hosted local LLMs

Used Vision models

Built a voice-enabled AI assistant

Created a scalable AI foundation

This is serious engineering.
