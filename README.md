# VoiceForge AI

### Voice-Controlled Multi-Agent AI System

VoiceForge AI is a voice-driven artificial intelligence system that combines speech recognition, local large language models, multi-agent orchestration, and text-to-speech to provide a conversational AI experience.

The project is designed around a modular agent architecture, allowing different AI agents to handle specialized reasoning tasks while providing a natural voice-based interface.

---

## Overview

Traditional conversational AI systems primarily rely on text input and output. VoiceForge AI extends this interaction model by integrating speech recognition and text-to-speech with a multi-agent AI architecture.

The application follows this workflow:

```text
User Voice
    │
    ▼
Audio Capture
    │
    ▼
Speech-to-Text
    │
    ▼
Agent Orchestrator
    │
    ├── Specialized Agent
    ├── Specialized Agent
    └── Specialized Agent
    │
    ▼
Local LLM
    │
    ▼
Generated Response
    │
    ▼
Text-to-Speech
    │
    ▼
Voice Response
```

This separation between the voice interface, orchestration layer, and individual agents makes the system easier to extend and experiment with.

---

## Key Features

* Voice-based interaction through microphone input
* Speech-to-text transcription using Whisper
* Local LLM inference through Ollama
* Multi-agent architecture for specialized reasoning
* Agent orchestration for coordinating AI tasks
* Text-to-speech response generation
* Audio file processing and playback
* Streamlit-based user interface
* Modular project structure for extending agent capabilities
* Local model execution without requiring a hosted LLM API for inference

---

## Architecture

VoiceForge AI is organized into several logical layers.

### Voice Input Layer

Handles microphone input and audio processing before sending the resulting audio to the speech recognition system.

```text
Microphone
    │
    ▼
Audio Capture
    │
    ▼
Audio Processing
    │
    ▼
Whisper
```

### Speech Recognition Layer

Whisper converts the user's spoken request into text.

```text
Audio
  │
  ▼
Whisper
  │
  ▼
Transcribed User Request
```

The resulting text becomes the input for the agent orchestration layer.

### Agent Orchestration Layer

The orchestrator determines how the request should be processed and coordinates the appropriate agents.

```text
User Request
     │
     ▼
Orchestrator
     │
     ├──────────────┐
     ▼              ▼
Agent A          Agent B
     │              │
     └──────┬───────┘
            ▼
        LLM Reasoning
```

This architecture allows additional agents to be introduced without requiring major changes to the voice interface.

### Response Layer

Once processing is complete, the generated response can be returned as text and converted into speech.

```text
Generated Response
        │
        ▼
  Text-to-Speech
        │
        ▼
   Voice Output
```

---

## Technology Stack

| Technology                | Purpose                        |
| ------------------------- | ------------------------------ |
| Python                    | Core application development   |
| Whisper                   | Speech-to-text transcription   |
| Ollama                    | Local LLM execution            |
| LLaMA / compatible models | Natural language reasoning     |
| pyttsx3                   | Text-to-speech                 |
| Streamlit                 | Web-based user interface       |
| sounddevice               | Audio capture                  |
| soundfile                 | Audio file handling            |
| pydub                     | Audio processing               |
| FFmpeg                    | Multimedia processing          |
| TinyDB                    | Lightweight local data storage |

---

## Project Structure

```text
voice-controlled-agent-ai/
│
├── agents/
│   └── Specialized AI agents
│
├── static/
│   └── Static application assets
│
├── templates/
│   └── Application templates
│
├── utils/
│   └── Utility modules
│
├── app.py
├── frontend.py
├── orchestrator.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Core Components

**`agents/`**

Contains the specialized AI agents responsible for individual reasoning tasks.

**`orchestrator.py`**

Coordinates interactions between the user request, agents, and language model.

**`frontend.py`**

Provides the Streamlit-based user interface.

**`app.py`**

Application-level entry point and supporting functionality.

**`utils/`**

Contains reusable utility functions used throughout the project.

---

# Installation

## Prerequisites

Before installing VoiceForge AI, make sure the following are available on your system:

* Python 3.8+
* Ollama
* A compatible local language model
* FFmpeg
* Working microphone
* Sufficient system memory for the selected language model

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

# Ollama Configuration

Install Ollama and make sure the Ollama service is running.

Pull the language model required by the project:

```bash
ollama pull llama2
```

Start the Ollama service if it is not already running:

```bash
ollama serve
```

> Use the model configured by the project if it differs from the example above.

---

# FFmpeg Configuration

FFmpeg is required for audio processing.

### Windows

Install FFmpeg and add its `bin` directory to the system `PATH`.

### macOS

```bash
brew install ffmpeg
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

Verify the installation:

```bash
ffmpeg -version
```

---

# Running the Application

Start the Streamlit interface:

```bash
streamlit run frontend.py
```

The application should become available at:

```text
http://localhost:8501
```

---

# Usage

Once the application is running:

1. Open the Streamlit interface in your browser.
2. Provide a voice input or supported audio input.
3. The audio is transcribed using Whisper.
4. The transcribed request is passed to the agent orchestration layer.
5. The appropriate agent or agents process the request using the configured language model.
6. The generated response is displayed to the user.
7. The response can be converted into speech through the text-to-speech layer.

A typical interaction looks like:

```text
Voice Input
     ↓
Whisper Transcription
     ↓
Agent Orchestration
     ↓
LLM Processing
     ↓
Generated Response
     ↓
Text-to-Speech
     ↓
Voice Output
```

---

# Multi-Agent Design

The system is designed to support specialized agents rather than relying entirely on a single conversational component.

This makes it possible to assign different responsibilities to different agents.

For example:

```text
                    User Request
                         │
                         ▼
                  Agent Orchestrator
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
        Research      Analysis   Summarization
          Agent         Agent        Agent
             │           │           │
             └───────────┼───────────┘
                         ▼
                    LLM Response
```

The modular design makes the system suitable for experimenting with additional agents, tools, memory systems, and more advanced routing strategies.

---

# Configuration

The language model and other runtime parameters can be configured according to the local environment and available resources.

For example:

```python
MODEL = "llama2"
```

The selected model should also be available through Ollama:

```bash
ollama list
```

If a different model is used, update the corresponding project configuration.

---

# Troubleshooting

### Ollama connection error

Make sure the Ollama service is running:

```bash
ollama serve
```

Then verify that the model is installed:

```bash
ollama list
```

### FFmpeg not found

Verify that FFmpeg is installed and available in the system `PATH`:

```bash
ffmpeg -version
```

### Missing Python packages

Reinstall the project dependencies:

```bash
pip install -r requirements.txt
```

### Microphone not detected

Check that:

* The microphone is connected.
* The operating system has granted microphone permissions.
* No other application is exclusively using the microphone.
* The correct audio input device is selected.

### Streamlit port already in use

Run the application on another port:

```bash
streamlit run frontend.py --server.port 8502
```

---

# Development Roadmap

Potential improvements include:

* Real-time streaming speech recognition
* Wake-word detection
* Voice activity detection
* Improved conversational memory
* Persistent long-term agent memory
* Additional specialized agents
* Tool and function calling
* Agent routing and planning
* Multi-language speech support
* Configurable voices and speech parameters
* Agent execution monitoring
* Improved error handling and recovery
* Support for additional local LLMs

---

# Contributing

Contributions and improvements are welcome.

To contribute:

```bash
git checkout -b feature/your-feature
```

Make your changes, then:

```bash
git add .
git commit -m "feat: describe your change"
git push origin feature/your-feature
```

Open a pull request with a clear description of the changes and their purpose.

---

# License

This project is available under the MIT License.

See the `LICENSE` file for more information.

---

# Author

**Esha Mirza**

GitHub: [Esha-Mirza](https://github.com/Esha-Mirza)

---

## Project Resources

* [OpenAI Whisper](https://github.com/openai/whisper)
* [Ollama](https://ollama.com/)
* [Streamlit](https://streamlit.io/)
* [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
* [FFmpeg](https://ffmpeg.org/)

---

<p align="center">
  <strong>VoiceForge AI</strong><br>
  Voice-controlled interaction with a modular multi-agent AI architecture.
</p>
