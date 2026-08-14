# 🎙️ VoiceForge AI

### Intelligent Voice-Controlled Multi-Agent System

<p align="center">
  <strong>Speak naturally. Delegate intelligently. Get your answers back through voice.</strong>
</p>

<p align="center">
  A privacy-focused voice AI system combining speech recognition, local LLM reasoning, multi-agent orchestration, and text-to-speech interaction.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-Speech--to--Text-412991?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-App%20UI-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

## ✨ Overview

**VoiceForge AI** is a voice-first multi-agent AI system designed to make interaction with intelligent agents more natural, accessible, and hands-free.

Instead of requiring users to type every request, VoiceForge AI creates a complete voice interaction loop:

```text
🎙️ User Speech
      ↓
🎧 Audio Capture
      ↓
📝 Speech-to-Text
      ↓
🧠 AI Agent Orchestration
      ↓
🤖 Specialized Agents
      ↓
💬 Generated Response
      ↓
🔊 Text-to-Speech
      ↓
👤 User Hears the Answer
```

The system combines **speech recognition**, **local large language models**, **multi-agent reasoning**, and **text-to-speech** into a single workflow.

A major design goal is **local-first AI**: the application can run without relying on paid cloud inference APIs, helping keep voice interactions and generated content on the user's machine.

---

## 🚀 Why VoiceForge AI?

Traditional AI assistants generally follow a simple:

> User → LLM → Response

architecture.

VoiceForge AI expands that concept by introducing a **multi-agent orchestration layer**.

Different agents can specialize in different reasoning tasks, allowing a single voice request to trigger a more structured AI workflow.

For example:

```text
                    ┌─────────────────┐
                    │   Voice Input   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │     Whisper     │
                    │ Speech-to-Text │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   Orchestrator  │
                    └────────┬────────┘
                             ↓
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
        ┌──────────┐   ┌───────────┐   ┌──────────┐
        │ Research │   │ Summarize │   │  Insight │
        │  Agent   │   │   Agent   │   │  Agent   │
        └────┬─────┘   └─────┬─────┘   └────┬─────┘
             └───────────────┼──────────────┘
                             ↓
                    ┌─────────────────┐
                    │   LLM Response  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │    pyttsx3      │
                    │ Text-to-Speech  │
                    └────────┬────────┘
                             ↓
                         🔊 Voice
```

---

## 🎯 Key Features

### 🎙️ Voice Interaction

Interact with the AI using your microphone instead of relying entirely on keyboard input.

### 📝 Speech-to-Text

Voice input is transcribed using **OpenAI Whisper**, converting spoken language into text that can be processed by the agent system.

### 🧠 Multi-Agent Architecture

The system is designed around specialized AI agents rather than a single monolithic chatbot.

Potential agent responsibilities include:

* Research
* Summarization
* Insight generation
* Devil's advocate / critical reasoning
* Voice interaction

### 🤖 Local LLM Inference

The project integrates with **Ollama** to run large language models locally.

This makes it possible to experiment with AI agents without requiring a paid hosted LLM API.

### 🔊 Text-to-Speech

AI responses can be converted back into spoken language using **pyttsx3**.

### 🎧 Audio File Support

The system can work with recorded audio in addition to direct microphone interaction.

### 🖥️ Interactive Interface

The application uses **Streamlit** to provide a simple browser-based interface for interacting with the agent system.

### 🔐 Privacy-Oriented Architecture

The project is designed around local processing, reducing the need to send voice data and prompts to external AI services.

### 💰 API-Free AI Workflow

By using local model inference through Ollama, the system can be used without per-request cloud inference costs.

---

## 🧩 Technology Stack

| Technology                        | Role                            |
| --------------------------------- | ------------------------------- |
| **Python**                        | Core application language       |
| **Whisper**                       | Speech-to-text transcription    |
| **Ollama**                        | Local LLM runtime               |
| **LLaMA / compatible local LLMs** | AI reasoning                    |
| **pyttsx3**                       | Text-to-speech                  |
| **Streamlit**                     | Interactive web interface       |
| **sounddevice**                   | Microphone/audio capture        |
| **soundfile**                     | Audio file handling             |
| **pydub**                         | Audio processing                |
| **TinyDB**                        | Lightweight local data storage  |
| **FFmpeg**                        | Audio conversion and processing |

---

## 🏗️ Architecture

VoiceForge AI separates the application into multiple responsibilities.

### 1. Voice Layer

Responsible for capturing and processing user audio.

```text
Microphone
    ↓
Audio Recording
    ↓
Whisper
    ↓
Transcribed Text
```

### 2. Agent Layer

The transcribed request is passed into the agent system.

```text
User Request
     ↓
Agent Orchestrator
     ↓
Specialized Agent
     ↓
LLM Reasoning
```

### 3. Response Layer

The generated response is returned to the user as both text and speech.

```text
AI Response
     ↓
pyttsx3
     ↓
Spoken Response
```

---

## 🧠 Multi-Agent Workflow

VoiceForge AI can expose specialized reasoning capabilities through voice commands.

| Voice Command                   | Agent / Action       |
| ------------------------------- | -------------------- |
| **"Summarize our discussion"**  | Summarization        |
| **"Challenge our assumptions"** | Devil's Advocate     |
| **"Give me key insights"**      | Insight generation   |
| **"Do a full analysis"**        | Multi-agent workflow |

This architecture makes the system extensible: additional specialized agents can be introduced without redesigning the entire voice interface.

---

## 📂 Project Structure

```text
voiceforge-ai/
│
├── agents/
│   ├── ...
│   └── ...
│
├── static/
│   └── ...
│
├── templates/
│   └── ...
│
├── utils/
│   └── ...
│
├── app.py
├── frontend.py
├── orchestrator.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Core Components

| Component          | Responsibility                     |
| ------------------ | ---------------------------------- |
| `agents/`          | Specialized AI-agent functionality |
| `orchestrator.py`  | Coordinates agent execution        |
| `frontend.py`      | User-facing application interface  |
| `app.py`           | Application entry point            |
| `utils/`           | Supporting utilities               |
| `templates/`       | UI templates                       |
| `static/`          | Static assets                      |
| `requirements.txt` | Python dependencies                |

---

# ⚙️ Installation

## Prerequisites

Before running VoiceForge AI, make sure you have:

* Python **3.8 or newer**
* Ollama
* A compatible local LLM
* FFmpeg
* A working microphone
* Approximately **8 GB+ RAM recommended**
* Sufficient disk space for local AI models

---

## 1. Clone the Repository

```bash
git clone https://github.com/Esha-Mirza/voice-controlled-agent-ai.git

cd voice-controlled-agent-ai
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🦙 Configure Ollama

Install Ollama and make sure the Ollama service is running.

Then download a compatible model.

For example:

```bash
ollama pull llama2
```

You can also use another compatible local model supported by your configuration.

Start Ollama with:

```bash
ollama serve
```

---

# 🎧 Configure FFmpeg

FFmpeg is required for audio processing.

### Windows

Install FFmpeg and add its `bin` directory to your system `PATH`.

### macOS

```bash
brew install ffmpeg
```

### Ubuntu / Debian

```bash
sudo apt install ffmpeg
```

---

# ▶️ Running the Application

Start the Streamlit interface:

```bash
streamlit run frontend.py
```

Then open:

```text
http://localhost:8501
```

---

# 🎤 Using VoiceForge AI

Once the application is running:

### Step 1 — Start a conversation

Create a new topic or select an existing conversation.

### Step 2 — Provide input

You can:

* 🎙️ Record your voice
* 📁 Upload an audio file
* ⌨️ Enter text manually

### Step 3 — Let the agents reason

Your request is transcribed and passed into the AI orchestration layer.

### Step 4 — Receive the result

The generated response is displayed and can be spoken back through text-to-speech.

---

# 🔄 Example Interaction

### User

> "What are the major trends in artificial intelligence?"

### VoiceForge AI

```text
🎙️ Voice Input
       ↓
📝 Whisper Transcription
       ↓
🧠 Agent Orchestrator
       ↓
🤖 AI Reasoning
       ↓
💬 Generated Response
       ↓
🔊 Text-to-Speech
```

The user can then hear the generated response without needing to read the entire answer.

---

# 🔧 Configuration

VoiceForge AI is designed to be configurable.

## Change the LLM

The local model can be changed through the agent configuration.

For example:

```python
MODEL = "llama2"
```

Depending on your Ollama installation, this can be replaced with another compatible model.

---

## Change Recording Duration

The recording duration can be configured through the Streamlit interface.

Example:

```python
recording_duration = st.slider(
    "Recording Duration (seconds)",
    3,
    15,
    5
)
```

---

## Configure Text-to-Speech

Voice properties such as speech rate and volume can be adjusted.

```python
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)
```

---

# 🛠️ Troubleshooting

| Problem                   | Possible Solution                     |
| ------------------------- | ------------------------------------- |
| Model not found           | Pull the required model with Ollama   |
| Ollama connection refused | Start `ollama serve`                  |
| Microphone unavailable    | Check OS microphone permissions       |
| FFmpeg not found          | Install FFmpeg and add it to `PATH`   |
| TTS unavailable           | Verify `pyttsx3` and system voices    |
| Python module missing     | Run `pip install -r requirements.txt` |
| Port already in use       | Start Streamlit using another port    |

Example:

```bash
streamlit run frontend.py --server.port 8502
```

---

# 🗺️ Roadmap

The project can be extended with several advanced capabilities:

* [ ] Wake-word detection
* [ ] Real-time streaming transcription
* [ ] Configurable TTS voices and accents
* [ ] Improved conversational memory
* [ ] More specialized AI agents
* [ ] Tool/function calling
* [ ] Agent performance monitoring
* [ ] Long-term memory
* [ ] Multi-language voice support
* [ ] Voice activity detection
* [ ] More advanced agent routing

---

# 🔮 Future Vision

The long-term goal of VoiceForge AI is to evolve from a voice-controlled chatbot into a **general-purpose local AI agent platform**.

The architecture can be extended toward:

```text
                 VoiceForge AI
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Voice       Agents       Tools
          │           │           │
          ↓           ↓           ↓
       Whisper     Local LLM    APIs / OS
          │           │           │
          └───────────┼───────────┘
                      ↓
                Agent Memory
                      ↓
              Intelligent Action
```

This provides a foundation for building more capable, privacy-conscious AI assistants.

---

# 🔐 Privacy

VoiceForge AI is designed with a local-first philosophy.

When configured with local inference through Ollama, AI processing can remain on the user's machine instead of requiring every request to be sent to a hosted LLM API.

However, users should review the configuration of any external services or models they add to the system before using the application with sensitive information.

---

# 📚 Learning Resources

The project builds on several excellent open-source technologies:

* [OpenAI Whisper](https://github.com/openai/whisper) — Speech recognition
* [Ollama](https://ollama.com/) — Local LLM runtime
* [Streamlit](https://streamlit.io/) — Interactive Python applications
* [pyttsx3](https://github.com/nateshmbhat/pyttsx3) — Text-to-speech
* [FFmpeg](https://ffmpeg.org/) — Multimedia processing

---

# 🤝 Contributing

Contributions, ideas, improvements, and experiments are welcome.

A typical contribution workflow:

```bash
git checkout -b feature/your-feature

git add .

git commit -m "feat: add your feature"

git push origin feature/your-feature
```

Then open a Pull Request describing the change.

---

# 📄 License

This project is released under the **MIT License**.

See the `LICENSE` file for details.

---

# 👩‍💻 Author

**Esha Mirza**

AI / Machine Learning Developer

[GitHub](https://github.com/Esha-Mirza)

---

<p align="center">
  <strong>🎙️ Voice in. Intelligence out.</strong>
</p>

<p align="center">
  Built with Python, Whisper, Ollama, and open-source AI.
</p>
