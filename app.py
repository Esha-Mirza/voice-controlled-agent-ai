from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from orchestrator import run_agent

from utils.voice_agent import (
    transcribe_audio,
    text_to_speech,
    stop_recording,
    stop_speech,
    is_recording,
    is_speaking
)


app = Flask(__name__)


@app.route("/")
def home():

    return render_template(
        "index.html",
        agents=[
            "Research",
            "Summarizer"
        ],
        default_duration=30
    )


@app.route(
    "/api/record",
    methods=["POST"]
)
def record_voice():

    data = (
        request.get_json(
            silent=True
        ) or {}
    )


    try:

        max_duration = int(
            data.get(
                "duration",
                30
            )
        )

    except (
        TypeError,
        ValueError
    ):

        max_duration = 30


    max_duration = max(
        10,
        min(
            max_duration,
            60
        )
    )


    try:

        print("")
        print(
            "=" * 50
        )

        print(
            "[VOICE] Starting recording..."
        )

        print(
            "=" * 50
        )


        result = transcribe_audio(
            max_duration=max_duration,
            silence_duration=3.0
        )


        print(
            f"[VOICE] Result: {result}"
        )


        if not result:

            return jsonify({
                "ok": False,
                "error":
                    "No speech was detected."
            }), 400


        if str(result).startswith(
            "Error"
        ):

            return jsonify({
                "ok": False,
                "error": result
            }), 400


        return jsonify({
            "ok": True,
            "transcribed": result
        })


    except Exception as error:

        print(
            f"[VOICE ERROR] {error}"
        )


        return jsonify({
            "ok": False,
            "error": str(error)
        }), 500


@app.route(
    "/api/stop-recording",
    methods=["POST"]
)
def api_stop_recording():

    stop_recording()


    return jsonify({
        "ok": True,
        "message":
            "Recording stop requested."
    })


@app.route(
    "/api/run-agent",
    methods=["POST"]
)
def run_agent_api():

    data = (
        request.get_json(
            silent=True
        ) or {}
    )


    text = str(
        data.get(
            "text",
            ""
        )
    ).strip()


    agent = str(
        data.get(
            "agent",
            "Research"
        )
    )


    if not text:

        return jsonify({
            "ok": False,
            "error":
                "No text to process."
        }), 400


    if agent not in {
        "Research",
        "Summarizer"
    }:

        return jsonify({
            "ok": False,
            "error":
                "Unknown agent selected."
        }), 400


    try:

        print(
            f"[AGENT] Running {agent}..."
        )


        response = run_agent(
            agent,
            text
        )


        print(
            "[AGENT] Response generated."
        )


        return jsonify({
            "ok": True,
            "response": response,
            "agent": agent
        })


    except Exception as error:

        print(
            f"[AGENT ERROR] {error}"
        )


        return jsonify({
            "ok": False,
            "error": str(error)
        }), 500


@app.route(
    "/api/speak",
    methods=["POST"]
)
def speak_api():

    data = (
        request.get_json(
            silent=True
        ) or {}
    )


    text = str(
        data.get(
            "text",
            ""
        )
    ).strip()


    if not text:

        return jsonify({
            "ok": False,
            "error":
                "No text to speak."
        }), 400


    try:

        text_to_speech(
            text
        )


        return jsonify({
            "ok": True
        })


    except Exception as error:

        print(
            f"[TTS ERROR] {error}"
        )


        return jsonify({
            "ok": False,
            "error": str(error)
        }), 500


@app.route(
    "/api/stop-speaking",
    methods=["POST"]
)
def stop_speaking_api():

    stop_speech()


    return jsonify({
        "ok": True,
        "message":
            "Speech stopped."
    })


@app.route(
    "/api/status",
    methods=["GET"]
)
def status():

    return jsonify({
        "ok": True,
        "recording":
            is_recording(),
        "speaking":
            is_speaking()
    })


@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify({
        "ok": True,
        "status": "online"
    })


if __name__ == "__main__":

    print("")
    print("=" * 55)
    print("VOICE-CONTROLLED AGENT SYSTEM")
    print("=" * 55)
    print(
        "Server: http://127.0.0.1:5000"
    )
    print(
        "Auto-stop: 3 seconds of silence"
    )
    print(
        "Maximum recording: 60 seconds"
    )
    print("=" * 55)
    print("")


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        threaded=True
    )