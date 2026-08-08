import whisper
import pyttsx3
import sounddevice as sd
import tempfile
import scipy.io.wavfile as wav
import numpy as np
import time

# Load Whisper model (cached)
model = None

def get_whisper_model():
    global model
    if model is None:
        model = whisper.load_model("base")
    return model

def transcribe_audio(duration: int = 5) -> str:
    """Record and transcribe audio using Whisper"""
    try:
        fs = 16000
        print(f"🎤 Recording for {duration} seconds...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        print("✅ Recording complete!")
        
        # Save temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav.write(tmp.name, fs, (recording * 32767).astype(np.int16))
            tmp_path = tmp.name
        
        # Transcribe
        whisper_model = get_whisper_model()
        result = whisper_model.transcribe(tmp_path)
        return result["text"].strip()
    except Exception as e:
        return f"Error in transcription: {str(e)}"

def text_to_speech(text: str):
    """Convert text to speech"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)
        engine.say(text[:500])
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {str(e)}")

def process_voice_command(command: str, agent_type: str = "Research") -> str:
    """Process voice command through the selected agent"""
    if agent_type == "Research":
        from agents.research_agent import run
        return run(command)
    elif agent_type == "Summarizer":
        from agents.summarizer_agent import run
        return run(command)
    return "Unknown agent"