# Voice-Controlled Agent System

A voice-enabled multi-agent system that allows users to interact with AI agents using speech-to-text and hear responses via text-to-speech.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Ollama](https://img.shields.io/badge/LLM-Ollama-black)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [FFmpeg Installation](#ffmpeg-installation)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Voice Commands](#voice-commands)
- [Sample Workflow](#sample-workflow)
- [Project Structure](#project-structure)
- [Voice Features Explained](#voice-features-explained)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## Overview

This application extends the AthenaCore multi-agent system by adding voice capabilities. Users can speak their questions and hear agent responses aloud, making research more accessible and hands-free. It is designed for researchers, professionals, and anyone who prefers voice interaction.

The application runs entirely locally, ensuring data privacy and eliminating API costs. It uses Ollama to host the LLaMA 2 model, Whisper for speech-to-text, pyttsx3 for text-to-speech, and Streamlit for the user interface.

---

## Features

- **Voice Input** — Speak your questions using your microphone
- **Speech-to-Text** — Converts voice to text using Whisper
- **Text-to-Speech** — Reads agent responses aloud using pyttsx3
- **Multi-Agent Support** — Works with all AthenaCore agents
- **Voice Commands** — Quick voice actions for common tasks
- **Audio File Upload** — Upload pre-recorded audio files
- **Privacy-Focused** — All processing happens locally, no data is sent to external servers
- **No API Costs** — Free to use with no usage limits

---

## Technology Stack

| Technology | Purpose |
|---|---|
| **Whisper** | Speech-to-text transcription |
| **pyttsx3** | Text-to-speech synthesis |
| **sounddevice** | Audio recording from microphone |
| **soundfile** | Audio file handling |
| **pydub** | Audio processing and conversion |
| **LLaMA 2** | Large Language Model for agent reasoning |
| **Ollama** | Local LLM hosting and inference |
| **TinyDB** | Lightweight JSON database for memory storage |
| **Streamlit** | Frontend user interface |

---

## Prerequisites

| Requirement | Details |
|---|---|
| **Python** | Version 3.8 or higher |
| **Ollama** | Installed and running |
| **LLaMA 2 Model** | Downloaded via Ollama |
| **FFmpeg** | Installed and added to PATH (for audio processing) |
| **Microphone** | Working microphone for voice input |
| **RAM** | 8GB+ recommended |
| **Storage** | 5GB+ free space for models |

---

## FFmpeg Installation

### Windows

1. Download FFmpeg from: [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/)
2. Download the **"ffmpeg-release-full.7z"** file
3. Extract it to `C:\ffmpeg`
4. Add `C:\ffmpeg\bin` to your system PATH

### Mac

```bash
brew install ffmpeg
```

### Ubuntu

```bash
sudo apt install ffmpeg
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Esha-Mirza/School_Of_AI_Internship.git
cd School_Of_AI_Internship/"Project-15 Voice-Controlled Agent System"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull LLaMA 2 Model via Ollama

```bash
ollama pull llama2
```

This downloads the LLaMA 2 model (~3.8 GB). Alternatively, you can use a smaller model:

```bash
ollama pull phi3        # 2.2 GB, faster inference
ollama pull gemma:2b    # 1.4 GB, lightest option
```

---

## Running the Application

**Terminal 1: Start Ollama Service**

```bash
ollama serve
```

**Terminal 2: Start Streamlit Frontend**

```bash
streamlit run frontend.py
```

The frontend will open at: `http://localhost:8501`

---

## Usage

1. Open your browser and navigate to `http://localhost:8501`
2. Create a new topic or select an existing one
3. Choose a voice input method:
   - **Start Recording** — Speak your question using your microphone
   - **Upload Audio File** — Upload a pre-recorded audio file
   - **Type Manually** — Type your question as an alternative

---

## Voice Commands

| Command | What It Does |
|---|---|
| "Summarize our discussion" | Runs the Summarizer Agent |
| "Challenge our assumptions" | Runs the Devil's Advocate Agent |
| "Give me key insights" | Runs the Insight Agent |
| "Do a full analysis" | Runs all agents in sequence |

---

## Sample Workflow

**Voice Input:**

```text
User (speaking): "What are the latest trends in AI?"
```

**Transcription:**

```text
Transcribed: "What are the latest trends in AI?"
```

**Agent Response:**

```text
Research Agent: The latest trends include generative AI, large language models, and multimodal systems...
```

**Voice Output:** The response is read aloud using text-to-speech.

---

## Project Structure

```
Project-15 Voice-Controlled Agent System/
├── agents/
│   ├── __init__.py
│   ├── base.py
│   ├── voice_agent.py      # Voice functionality
│   ├── research_agent.py
│   ├── summarizer_agent.py
│   ├── devil_agent.py
│   └── insight_agent.py
├── memory/
│   ├── .gitkeep
│   └── memory_store.json
├── orchestrator.py
├── frontend.py              # Updated with voice features
├── requirements.txt
└── README.md
```

---

## Voice Features Explained

### Speech-to-Text (Whisper)

```text
Audio Input → Whisper Model → Text Output
```

- Uses OpenAI's Whisper model for accurate transcription
- Supports various audio formats and microphone input
- First run downloads the Whisper model (~1 GB)

### Text-to-Speech (pyttsx3)

```text
Text Output → pyttsx3 Engine → Audio Output
```

- Reads agent responses aloud
- Configurable voice speed and volume
- Works offline with system voices

### Audio Recording (sounddevice)

```text
Microphone → sounddevice Recording → Audio Data
```

- Records audio from your microphone
- Configurable recording duration (3-15 seconds)
- Converts to format suitable for Whisper

---

## Configuration

### Changing the Model

To use a different LLM model, modify `agents/base.py`:

```python
MODEL = "phi3"        # Change from "llama2" to your preferred model
```

### Changing Recording Duration

To adjust the default recording duration, modify the slider in the UI:

```python
recording_duration = st.slider("Recording Duration (seconds)", 3, 15, 5)
```

### Changing Voice Settings

To change TTS voice settings, modify `agents/voice_agent.py`:

```python
engine.setProperty('rate', 180)    # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
```

### Changing the Port

```bash
streamlit run frontend.py --server.port 8502
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Model not found | Run `ollama pull llama2` to download the model |
| Connection refused | Ensure Ollama is running (`ollama serve`) |
| Microphone not found | Check your microphone settings in Control Panel |
| FFmpeg not found | Install FFmpeg and add to PATH |
| Whisper model error | First run downloads the model — be patient |
| TTS not working | Ensure pyttsx3 is installed and system voices are available |
| Port already in use | Use `--server.port` flag to specify a different port |
| Module not found | Run `pip install -r requirements.txt` |

---

## Roadmap

- [ ] Add wake-word detection for hands-free activation (no button press needed)
- [ ] Add selectable TTS voices/accents
- [ ] Add live transcription streaming instead of record-then-transcribe

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Acknowledgments

- OpenAI Whisper - Speech recognition
- pyttsx3 - Text-to-speech
- [Ollama](https://ollama.com/) - Local LLM runtime
- Streamlit - UI framework

---

## Contact

- **GitHub:** [Esha-Mirza](https://github.com/Esha-Mirza)
- **Email:** esha101374@gmail.com
