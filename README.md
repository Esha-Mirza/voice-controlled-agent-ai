<h1 align="center"> VoiceForge AI </h1>

<p align="center">
  <strong>Voice-controlled interaction with local AI agents.</strong>
</p>

<p align="center">
  Speak naturally, let a local AI agent process your request, and receive the response as both text and speech — using Whisper, Ollama, TinyLlama, and Streamlit.
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.8%2B-3776AB?logo=python&logoColor=white" alt="Python 3.8+">
  </a>
  <a href="https://ollama.com/">
    <img src="https://img.shields.io/badge/Ollama-local%20LLM-black?logo=ollama&logoColor=white" alt="Ollama">
  </a>
  <a href="https://github.com/openai/whisper">
    <img src="https://img.shields.io/badge/Whisper-speech--to--text-412991?logo=openai&logoColor=white" alt="Whisper">
  </a>
  <a href="https://streamlit.io/">
    <img src="https://img.shields.io/badge/Streamlit-interface-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  </a>
  <img src="https://img.shields.io/badge/LLM-TinyLlama-blueviolet" alt="TinyLlama">
  <img src="https://img.shields.io/badge/TTS-pyttsx3-orange" alt="pyttsx3">
</p>

---

## Overview

VoiceForge AI is a voice-enabled multi-agent system that connects speech recognition, local language-model inference, agent orchestration, and text-to-speech into a single conversational workflow.

The application captures speech through the microphone, transcribes it using Whisper, sends the resulting text to a selected AI agent, and optionally reads the generated response aloud using `pyttsx3`.

The current application provides a Streamlit interface with agent selection, configurable recording duration, voice-output controls, transcription display, and response generation.

```text
Voice Input
     │
     ▼
Audio Capture
     │
     ▼
Whisper
     │
     ▼
Transcribed Text
     │
     ▼
Agent Orchestrator
     │
     ├── Research Agent
     └── Summarizer Agent
     │
     ▼
Ollama
     │
     ▼
TinyLlama
     │
     ▼
Agent Response
     │
     ├── Text Output
     │
     └── pyttsx3
            │
            ▼
       Voice Output
```

---

## Why VoiceForge AI?

Text-based interfaces are powerful, but they are not always the most natural way to interact with an AI system.

VoiceForge AI explores a different interaction model:

```text
Speak → Transcribe → Reason → Respond → Listen
```

The project combines several independent components into one workflow:

* **Whisper** handles speech recognition.
* **Ollama** provides local LLM inference.
* **TinyLlama** performs language-model reasoning.
* **The agent layer** provides task-specific behavior.
* **Streamlit** provides the interaction interface.
* **pyttsx3** converts generated responses back into speech.

Because the LLM is accessed through a locally running Ollama instance, the core AI inference workflow does not require a hosted LLM API. The model configuration currently points to `tinyllama` at Ollama's local generation endpoint.

---

## Features

### Voice Input

Record questions directly through the system microphone.

The application captures audio at 16 kHz and performs basic speech-activity detection while recording. Recording can stop when the configured maximum duration is reached or when silence is detected after speech.

### Speech-to-Text

Whisper converts recorded audio into text.

The current implementation loads the Whisper `base` model and transcribes the temporary WAV recording locally.

```text
Microphone
    │
    ▼
Audio Stream
    │
    ▼
Speech Detection
    │
    ▼
Temporary WAV
    │
    ▼
Whisper Base
    │
    ▼
Transcribed Text
```

### Agent Selection

The interface currently provides two selectable agents:

* Research
* Summarizer

The orchestrator routes the selected agent to its corresponding implementation.

### Local LLM Inference

The project uses Ollama to communicate with a locally hosted language model.

The current model configuration is:

```python
MODEL = "tinyllama"
```

and requests are sent to:

```text
http://localhost:11434/api/generate
```

The model call is handled centrally through `agents/base.py`.

### Text-to-Speech

Generated responses can be converted into speech using `pyttsx3`.

The implementation initializes the speech engine, configures the speech rate and volume, and runs speech output in a separate thread.

### Configurable Recording

The Streamlit interface provides a recording-duration control.

The current UI exposes a recording-duration slider between 3 and 10 seconds, while the underlying recorder also enforces minimum duration and silence-detection constraints.

### Manual Text Visibility

The interface displays the transcribed request in a text area before showing the agent response, making the speech-to-text stage visible to the user.

---

## Architecture

VoiceForge AI separates the application into four main layers:

```text
┌──────────────────────────────────────┐
│              Streamlit              │
│                                      │
│  Recording · Agent Selection         │
│  Transcription · Response · Controls │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│            Voice Layer               │
│                                      │
│     sounddevice → Whisper Base       │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Agent Orchestration         │
│                                      │
│     Research      │      Summarizer  │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│            LLM Layer                 │
│                                      │
│              Ollama                  │
│                 │                    │
│             TinyLlama                │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Response Layer              │
│                                      │
│        Text → pyttsx3 → Audio       │
└──────────────────────────────────────┘
```

---

## Request Lifecycle

A typical request passes through the following stages:

### 1. Capture

The user selects an agent and starts recording.

The Streamlit frontend calls the voice-processing layer to capture microphone input.

### 2. Speech Detection

The recorder monitors incoming audio and calculates signal volume to determine whether speech is present.

The implementation uses a configurable silence threshold and automatically stops after a period of detected silence.

### 3. Transcription

The recorded audio is written to a temporary WAV file and passed to Whisper.

```text
Audio → Temporary WAV → Whisper → Text
```

The temporary file is removed after transcription.

### 4. Agent Routing

The transcribed text is passed to:

```python
run_agent(agent_choice, result)
```

The orchestrator currently routes requests to either the Research or Summarizer agent.

### 5. LLM Inference

The selected agent uses the configured LLM layer, which sends the prompt to the locally running Ollama server.

```text
Agent
  │
  ▼
call_llm()
  │
  ▼
Ollama API
  │
  ▼
TinyLlama
```

The current LLM wrapper uses a non-streaming request with a 30-second timeout and a maximum token setting of 300.

### 6. Response

The generated response is displayed in Streamlit.

If voice output is enabled, the response is also passed to `text_to_speech()`. The current frontend limits the spoken response to the first 500 characters.

---

## Voice Processing

The voice pipeline is intentionally separated from the user interface.

```text
sounddevice
     │
     ▼
Audio Capture
     │
     ▼
Speech Detection
     │
     ▼
WAV File
     │
     ▼
Whisper Base
     │
     ▼
Text
```

### Speech Detection

The recorder processes audio in short blocks and calculates the RMS-like volume of incoming samples.

A threshold is used to determine when speech is active. If speech has already been detected and the volume remains below the threshold for the configured silence duration, recording stops.

This provides a simple turn-detection mechanism without requiring a separate voice-activity-detection service.

---

## Text-to-Speech

The response pipeline works in the opposite direction:

```text
Agent Response
      │
      ▼
pyttsx3
      │
      ▼
System Voice
      │
      ▼
Audio Output
```

The current implementation configures:

```python
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)
```

and manages speech execution using a background thread.

This allows the Streamlit interface to remain responsive while speech is being generated.

---

## Agent Architecture

The agent orchestration layer currently exposes two agents:

```text
                    User Request
                         │
                         ▼
                  Agent Orchestrator
                         │
               ┌─────────┴─────────┐
               │                   │
               ▼                   ▼
        Research Agent       Summarizer Agent
               │                   │
               └─────────┬─────────┘
                         ▼
                    LLM Inference
                         │
                         ▼
                      Response
```

The routing logic is intentionally small:

```python
def run_agent(agent, query=""):
    if agent == "Research":
        return research_agent.run(query)

    elif agent == "Summarizer":
        return summarizer_agent.run(query)

    return "Unknown agent"
```

This provides a simple foundation for adding additional specialized agents later.

---

## Example Interaction

A typical interaction looks like:

```text
User:
"What are the latest trends in artificial intelligence?"

        ↓

Voice Capture

        ↓

Whisper:
"What are the latest trends in artificial intelligence?"

        ↓

Research Agent

        ↓

TinyLlama via Ollama

        ↓

Generated Response

        ↓

Streamlit
        │
        └── pyttsx3 → Spoken Response
```

The important design principle is that voice is treated as an input/output layer around the underlying agent system rather than being tightly coupled to the language model.

---

## Technology Stack

| Technology  | Role                                |
| ----------- | ----------------------------------- |
| Python      | Application development             |
| Streamlit   | User interface                      |
| Whisper     | Speech-to-text                      |
| TinyLlama   | Local language model                |
| Ollama      | Local LLM runtime                   |
| pyttsx3     | Text-to-speech                      |
| sounddevice | Microphone capture                  |
| SciPy       | WAV/audio processing                |
| NumPy       | Audio signal processing             |
| Requests    | Ollama API communication            |
| FFmpeg      | Audio processing support            |
| TinyDB      | Lightweight data storage dependency |

The repository's current dependency file includes Whisper, pyttsx3, sounddevice, soundfile, pydub, FastAPI, Streamlit, Requests, Torch, and related packages.

---

## Requirements

Recommended environment:

| Requirement | Recommendation                                    |
| ----------- | ------------------------------------------------- |
| Python      | 3.8+                                              |
| RAM         | 8 GB+                                             |
| Storage     | 5 GB+ free                                        |
| Microphone  | Required for voice input                          |
| Ollama      | Required                                          |
| Local LLM   | TinyLlama or compatible Ollama model              |
| FFmpeg      | Required for supported audio-processing workflows |

The project currently uses a Whisper `base` model, which is downloaded when the Whisper model is first loaded.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Esha-Mirza/voice-controlled-agent-ai.git
cd voice-controlled-agent-ai
```

The repository is currently hosted at `Esha-Mirza/voice-controlled-agent-ai`.

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

The repository includes a pinned dependency set covering Streamlit, Whisper, Torch, pyttsx3, sounddevice, SciPy, Requests, and other supporting packages.

---

# Ollama Setup

Install Ollama and make sure it is running locally.

Download the model configured by the project:

```bash
ollama pull tinyllama
```

Verify the installation:

```bash
ollama list
```

You can test the model directly:

```bash
ollama run tinyllama
```

The application currently expects Ollama's local generation endpoint:

```text
http://localhost:11434/api/generate
```

and uses `tinyllama` as the configured model.

---

# FFmpeg Setup

FFmpeg may be required for audio-processing workflows and related dependencies.

### Windows

Install FFmpeg and add its `bin` directory to your system `PATH`.

Then verify:

```bash
ffmpeg -version
```

### macOS

```bash
brew install ffmpeg
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

---

# Running the Application

Start Ollama first:

```bash
ollama serve
```

Then open another terminal and run:

```bash
streamlit run frontend.py
```

The Streamlit application will normally be available at:

```text
http://localhost:8501
```

The current frontend is implemented entirely through Streamlit and imports the voice-processing functions from `utils.voice_agent`.

---

# Usage

Once the application is running:

### 1. Select an agent

Choose between:

* Research
* Summarizer

### 2. Configure recording

Use the recording-duration slider in the sidebar.

### 3. Start recording

Click **Start Recording** and speak into the configured microphone.

### 4. Transcription

Whisper processes the captured audio and displays the resulting text.

### 5. Agent processing

The selected agent receives the transcribed request and generates a response using the local LLM.

### 6. Voice output

If voice output is enabled, the response is spoken using `pyttsx3`.

The current Streamlit implementation exposes these controls directly in the UI.

---

## Configuration

### Change the LLM

The model is configured in:

```text
agents/base.py
```

Current configuration:

```python
MODEL = "tinyllama"
```

To use another Ollama-compatible model:

```python
MODEL = "phi3"
```

Then make sure the model is installed:

```bash
ollama pull phi3
```

The model name must match an installed model in your Ollama environment.

---

### Change the Ollama Endpoint

The current endpoint is defined in:

```text
agents/base.py
```

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
```

If Ollama is configured on another host or port, update this value accordingly.

---

### Change Recording Duration

The frontend currently exposes:

```python
st.slider(
    "Recording Duration (seconds)",
    3,
    10,
    5
)
```

The value is passed to the audio-recording function.

---

### Change Speech Settings

Text-to-speech settings are configured in:

```text
utils/voice_agent.py
```

For example:

```python
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)
```

Increase `rate` for faster speech or decrease it for slower speech. Volume accepts values between `0.0` and `1.0`.

---

## Project Structure

```text
voice-controlled-agent-ai/
│
├── agents/
│   ├── base.py
│   ├── research_agent.py
│   └── summarizer_agent.py
│
├── static/
│
├── templates/
│
├── utils/
│   └── voice_agent.py
│
├── app.py
├── frontend.py
├── orchestrator.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `agents/`

Contains the language-model and agent implementations.

### `agents/base.py`

Provides the Ollama model configuration and LLM request function. The current configuration uses TinyLlama through Ollama's local API.

### `agents/research_agent.py`

Implements the research-oriented agent used by the orchestrator.

### `agents/summarizer_agent.py`

Implements the summarization-oriented agent used by the orchestrator.

### `utils/voice_agent.py`

Contains the voice-processing functionality, including:

* Whisper model loading
* Microphone recording
* Speech detection
* Audio conversion
* Speech transcription
* Text-to-speech
* Speech-thread management

### `orchestrator.py`

Routes requests to the selected agent.

### `frontend.py`

Contains the Streamlit application and user interface.

---

## Local Processing

The core workflow can operate without a cloud LLM API:

```text
Microphone
    │
    ▼
Whisper
    │
    ▼
Local Agent
    │
    ▼
Ollama
    │
    ▼
TinyLlama
    │
    ▼
pyttsx3
    │
    ▼
Speaker
```

This architecture keeps the primary speech and LLM processing components on the local machine.

However, local processing does not automatically guarantee complete privacy for every possible future extension of the project. Any external services or APIs added later should be evaluated separately.

---

## Performance Considerations

Local AI workloads are dependent on the available hardware.

The main factors affecting performance are:

* CPU performance
* GPU availability
* Available RAM
* Whisper model size
* LLM size
* Audio length
* Number of concurrent operations

The current project uses the Whisper `base` model and TinyLlama, providing a relatively lightweight starting point for local experimentation.

For more capable reasoning, a larger Ollama model can be configured, but inference requirements will increase accordingly.

---

## Limitations

The current implementation is a focused prototype rather than a production-grade real-time voice-agent platform.

Current limitations include:

* Recording is not yet continuous streaming.
* Wake-word activation is not implemented.
* The orchestrator currently exposes Research and Summarizer agents.
* Voice output depends on locally available system voices.
* Model response quality depends heavily on the selected local LLM.
* Local inference can be slower than hosted GPU-backed APIs.
* The application currently processes a voice turn before generating the response rather than maintaining a continuous conversational audio stream.

These limitations also provide clear directions for future development.

---

## Roadmap

### Voice

* [ ] Wake-word detection
* [ ] Real-time streaming transcription
* [ ] Improved voice activity detection
* [ ] Configurable TTS voices
* [ ] Configurable speech accents
* [ ] Continuous conversation mode

### Agents

* [ ] Additional specialized agents
* [ ] Dynamic agent routing
* [ ] Agent planning
* [ ] Tool calling
* [ ] Persistent conversational memory
* [ ] Agent execution history

### Models

* [ ] Support for multiple Ollama models
* [ ] Runtime model selection
* [ ] Model-specific configuration
* [ ] Streaming LLM responses

### Interface

* [ ] Conversation history
* [ ] Audio playback controls
* [ ] Better error reporting
* [ ] Real-time transcription display
* [ ] Configurable audio devices

---

## Troubleshooting

### Ollama connection refused

Make sure Ollama is running:

```bash
ollama serve
```

Then verify:

```bash
ollama list
```

---

### Model not found

Install the configured model:

```bash
ollama pull tinyllama
```

Then verify:

```bash
ollama run tinyllama
```

---

### Microphone not detected

Check:

* The microphone is connected.
* The operating system has granted microphone permissions.
* The correct input device is selected.
* No other application is exclusively using the microphone.

---

### Whisper takes a long time on first run

The Whisper model is loaded lazily when transcription is first requested. The current implementation uses:

```python
whisper.load_model("base")
```

The initial model download and loading can therefore take longer than subsequent transcriptions.

---

### Text-to-speech does not work

Verify that `pyttsx3` is installed:

```bash
pip install pyttsx3
```

Also make sure your operating system has at least one available speech voice.

---

### FFmpeg not found

Verify:

```bash
ffmpeg -version
```

If the command is not recognized, install FFmpeg and add it to the system `PATH`.

---

### Port already in use

Run Streamlit on another port:

```bash
streamlit run frontend.py --server.port 8502
```

---

### Missing Python modules

Reinstall the project dependencies:

```bash
pip install -r requirements.txt
```

---

## Design Decisions

### Why Whisper?

Whisper provides a strong open-source speech-recognition component that can be run locally and integrates naturally with Python.

### Why Ollama?

Ollama provides a simple local interface for running language models and allows the agent layer to communicate with the model through a local HTTP endpoint.

### Why TinyLlama?

TinyLlama provides a relatively lightweight local model suitable for experimentation on systems that may not have the resources required by larger models.

The model is configurable, so the project can be adapted to other Ollama-compatible models.

### Why Streamlit?

Streamlit allows the complete voice interaction workflow to be exposed through a Python-based web interface without requiring a separate frontend stack.

### Why an Orchestrator?

The orchestrator separates agent selection from the Streamlit interface, making it possible to add new agents without rewriting the application's main interaction flow.

---

## Future Architecture

The current architecture provides a foundation for a more advanced voice-agent system.

A future version could evolve toward:

```text
                         VoiceForge AI
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
             Voice         Agent         Memory
             Layer         Router         Layer
                │             │             │
                └─────────────┼─────────────┘
                              │
                              ▼
                         Tool Layer
                              │
                 ┌────────────┼────────────┐
                 │            │            │
                 ▼            ▼            ▼
              Search       APIs        Local Tools
                 │            │            │
                 └────────────┼────────────┘
                              ▼
                           Local LLM
                              │
                              ▼
                         Voice Response
```

This would allow the project to move from a voice interface around a small set of agents toward a more general local voice-agent framework.

---

## Contributing

Contributions and improvements are welcome.

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Make your changes:

```bash
git add .
git commit -m "feat: describe your change"
```

Push the branch:

```bash
git push origin feature/your-feature
```

Then open a pull request describing:

* What changed
* Why the change was made
* How it was tested
* Any additional setup required

---

## License

This project is released under the MIT License.

---

## Acknowledgments

* [OpenAI Whisper](https://github.com/openai/whisper) — Speech recognition
* [Ollama](https://ollama.com/) — Local LLM runtime
* [Streamlit](https://streamlit.io/) — Application interface
* [pyttsx3](https://github.com/nateshmbhat/pyttsx3) — Text-to-speech

---

## Author

**Esha Mirza**

[GitHub](https://github.com/Esha-Mirza)

---

<p align="center">
  <strong>VoiceForge AI</strong><br>
  Local voice interaction with AI agents.
</p>
