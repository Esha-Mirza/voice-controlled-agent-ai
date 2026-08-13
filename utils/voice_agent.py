import whisper
import pyttsx3
import sounddevice as sd
import tempfile
import scipy.io.wavfile as wav
import numpy as np
import threading
import time
import os


model = None


recording_active = False
recording_stop_event = threading.Event()
recording_lock = threading.Lock()


speech_active = False
speech_stop_event = threading.Event()
speech_lock = threading.Lock()

current_engine = None
speech_thread = None


def get_whisper_model():

    global model

    if model is None:

        print("Loading Whisper model...")

        model = whisper.load_model("base")

        print("Whisper model loaded.")

    return model


def transcribe_audio(
    max_duration: int = 30,
    silence_duration: float = 3.0
) -> str:

    global recording_active

    try:

        fs = 16000

        max_duration = max(
            10,
            int(max_duration)
        )

        silence_duration = max(
            2.0,
            float(silence_duration)
        )

        recording_stop_event.clear()

        with recording_lock:

            recording_active = True

        print("")
        print("🎤 Listening...")
        print(
            f"Maximum recording time: {max_duration} seconds"
        )
        print(
            f"Automatic stop after {silence_duration:.1f} seconds of silence"
        )

        audio_chunks = []

        speech_detected = False

        silence_started = None

        start_time = time.time()

        block_duration = 0.1

        block_size = int(
            fs * block_duration
        )

        silence_threshold = 0.012


        def audio_callback(
            indata,
            frames,
            callback_time,
            status
        ):

            if status:

                print(
                    f"Audio status: {status}"
                )

            audio_chunks.append(
                indata.copy()
            )


        with sd.InputStream(
            samplerate=fs,
            channels=1,
            dtype="float32",
            blocksize=block_size,
            callback=audio_callback
        ):

            previous_chunks = 0

            while True:

                if recording_stop_event.is_set():

                    print(
                        "🛑 Recording stopped manually."
                    )

                    break


                elapsed = (
                    time.time()
                    - start_time
                )


                if elapsed >= max_duration:

                    print(
                        "⏱ Maximum recording time reached."
                    )

                    break


                current_chunks = len(
                    audio_chunks
                )


                if current_chunks > previous_chunks:

                    new_chunks = audio_chunks[
                        previous_chunks:current_chunks
                    ]

                    previous_chunks = current_chunks


                    current_audio = np.concatenate(
                        new_chunks,
                        axis=0
                    )


                    volume = float(
                        np.sqrt(
                            np.mean(
                                np.square(
                                    current_audio
                                )
                            )
                        )
                    )


                    if volume > silence_threshold:

                        if not speech_detected:

                            speech_detected = True

                            print(
                                "🎙 Speech detected..."
                            )

                        silence_started = None

                    else:

                        if speech_detected:

                            if silence_started is None:

                                silence_started = (
                                    time.time()
                                )

                            silence_time = (
                                time.time()
                                - silence_started
                            )


                            if (
                                silence_time
                                >= silence_duration
                            ):

                                print(
                                    "🔇 3 seconds of silence detected."
                                )

                                break


                time.sleep(
                    0.05
                )


        with recording_lock:

            recording_active = False


        if not audio_chunks:

            return (
                "Error: No audio was recorded."
            )


        recording = np.concatenate(
            audio_chunks,
            axis=0
        )


        if len(recording) == 0:

            return (
                "Error: No audio was recorded."
            )


        if not speech_detected:

            return (
                "Error: No speech was detected."
            )


        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as tmp:

            wav.write(
                tmp.name,
                fs,
                (
                    recording * 32767
                ).astype(np.int16)
            )

            tmp_path = tmp.name


        try:

            print(
                "🧠 Transcribing with Whisper..."
            )

            whisper_model = (
                get_whisper_model()
            )

            result = (
                whisper_model.transcribe(
                    tmp_path
                )
            )

            text = (
                result
                .get("text", "")
                .strip()
            )


            if not text:

                return (
                    "Error: No speech was detected."
                )


            print(
                f"✅ Transcription: {text}"
            )

            return text


        finally:

            try:

                os.remove(
                    tmp_path
                )

            except OSError:

                pass


    except Exception as error:

        with recording_lock:

            recording_active = False

        return (
            f"Error in transcription: {str(error)}"
        )


def stop_recording():

    recording_stop_event.set()

    print(
        "🛑 Recording stop requested."
    )


def is_recording():

    with recording_lock:

        return recording_active


def text_to_speech(text: str):

    global speech_active
    global speech_thread
    global current_engine


    if not text:

        return


    stop_speech()

    speech_stop_event.clear()


    def speak():

        global speech_active
        global current_engine


        engine = None


        try:

            speech_active = True


            print(
                "🔊 Speaking..."
            )


            engine = pyttsx3.init()


            with speech_lock:

                current_engine = engine


            engine.setProperty(
                "rate",
                180
            )

            engine.setProperty(
                "volume",
                1.0
            )


            if speech_stop_event.is_set():

                return


            engine.say(
                text[:500]
            )


            engine.runAndWait()


        except Exception as error:

            if not speech_stop_event.is_set():

                print(
                    f"TTS Error: {str(error)}"
                )


        finally:

            try:

                if engine is not None:

                    engine.stop()

            except Exception:

                pass


            with speech_lock:

                if current_engine is engine:

                    current_engine = None


            speech_active = False


            print(
                "🔊 Speech finished."
            )


    speech_thread = threading.Thread(
        target=speak,
        daemon=True
    )


    speech_thread.start()


def stop_speech():

    global speech_active
    global current_engine


    speech_stop_event.set()


    with speech_lock:

        engine = current_engine


    if engine is not None:

        try:

            engine.stop()

            print(
                "🛑 Current speech stopped."
            )

        except Exception as error:

            print(
                f"TTS stop error: {error}"
            )


    speech_active = False


def is_speaking():

    return speech_active


def process_voice_command(
    command: str,
    agent_type: str = "Research"
) -> str:

    if agent_type == "Research":

        from agents.research_agent import run

        return run(command)


    elif agent_type == "Summarizer":

        from agents.summarizer_agent import run

        return run(command)


    return "Unknown agent"