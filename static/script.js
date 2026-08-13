document.addEventListener(
    "DOMContentLoaded",
    function () {

        const recordButton =
            document.getElementById(
                "record-button"
            );

        const recordButtonText =
            document.getElementById(
                "record-button-text"
            );

        const durationInput =
            document.getElementById(
                "duration"
            );

        const durationValue =
            document.getElementById(
                "duration-value"
            );

        const agentSelect =
            document.getElementById(
                "agent-select"
            );

        const voiceOutput =
            document.getElementById(
                "voice-output"
            );

        const transcription =
            document.getElementById(
                "transcription"
            );

        const responsePanel =
            document.getElementById(
                "response-panel"
            );

        const response =
            document.getElementById(
                "response"
            );

        const speakButton =
            document.getElementById(
                "speak-button"
            );

        const clearButton =
            document.getElementById(
                "clear-button"
            );

        const errorMessage =
            document.getElementById(
                "error-message"
            );

        const voiceState =
            document.getElementById(
                "voice-state"
            );

        const voiceDescription =
            document.getElementById(
                "voice-description"
            );

        const statusText =
            document.getElementById(
                "status-text"
            );

        const orbContainer =
            document.getElementById(
                "orb-container"
            );

        const voiceCard =
            document.querySelector(
                ".voice-card"
            );


        let recording = false;

        let processing = false;

        let speaking = false;


        if (!recordButton) {

            console.error(
                "record-button not found."
            );

            return;
        }


        if (!transcription) {

            console.error(
                "transcription element not found."
            );

            return;
        }


        if (!response) {

            console.error(
                "response element not found."
            );

            return;
        }


        if (durationInput) {

            durationInput.min = "10";

            durationInput.max = "60";

            durationInput.value = "30";

        }


        if (durationValue) {

            durationValue.textContent =
                "30s max";

        }


        if (durationInput) {

            durationInput.addEventListener(
                "input",
                function () {

                    durationValue.textContent =
                        durationInput.value +
                        "s max";

                }
            );

        }


        function setStatus(
            title,
            description
        ) {

            if (voiceState) {

                voiceState.textContent =
                    title;

            }


            if (voiceDescription) {

                voiceDescription.textContent =
                    description;

            }

        }


        function setSystemStatus(
            status
        ) {

            if (statusText) {

                statusText.textContent =
                    status;

            }

        }


        function showError(
            message
        ) {

            if (!errorMessage) {

                return;

            }


            errorMessage.textContent =
                message;


            errorMessage.classList.remove(
                "hidden"
            );

        }


        function hideError() {

            if (!errorMessage) {

                return;

            }


            errorMessage.textContent =
                "";


            errorMessage.classList.add(
                "hidden"
            );

        }


        function setRecordingVisual(
            active
        ) {

            if (orbContainer) {

                if (active) {

                    orbContainer.classList.add(
                        "recording"
                    );

                } else {

                    orbContainer.classList.remove(
                        "recording"
                    );

                }

            }


            if (voiceCard) {

                if (active) {

                    voiceCard.classList.add(
                        "recording"
                    );

                } else {

                    voiceCard.classList.remove(
                        "recording"
                    );

                }

            }

        }


        function updateRecordButton() {

            if (recording) {

                recordButtonText.textContent =
                    "Stop Recording";


                recordButton.classList.add(
                    "stop-mode"
                );

            } else {

                recordButtonText.textContent =
                    "Start Recording";


                recordButton.classList.remove(
                    "stop-mode"
                );

            }

        }


        function updateSpeakButton() {

            if (!speakButton) {

                return;

            }


            if (speaking) {

                speakButton.textContent =
                    "⏹ Stop Speaking";


                speakButton.classList.add(
                    "stop-mode"
                );

            } else {

                speakButton.textContent =
                    "🔊 Speak Response";


                speakButton.classList.remove(
                    "stop-mode"
                );

            }

        }


        async function startRecording() {

            if (recording) {

                return;

            }


            if (processing) {

                return;

            }


            if (speaking) {

                await stopSpeaking();

            }


            hideError();


            recording = true;

            processing = true;


            updateRecordButton();

            setRecordingVisual(
                true
            );


            setStatus(
                "Listening...",
                "Speak now. Recording will stop after 3 seconds of silence."
            );


            setSystemStatus(
                "LISTENING"
            );


            transcription.innerHTML =
                '<span class="placeholder">' +
                "Listening for your voice..." +
                "</span>";


            responsePanel.classList.add(
                "hidden"
            );


            try {

                const serverResponse =
                    await fetch(
                        "/api/record",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({

                                    duration:
                                        durationInput
                                            ? parseInt(
                                                durationInput.value,
                                                10
                                            )
                                            : 30

                                })
                        }
                    );


                const data =
                    await serverResponse.json();


                if (
                    !serverResponse.ok ||
                    !data.ok
                ) {

                    throw new Error(
                        data.error ||
                        "Recording failed."
                    );

                }


                const spokenText =
                    (
                        data.transcribed ||
                        ""
                    ).trim();


                if (!spokenText) {

                    throw new Error(
                        "No speech was detected."
                    );

                }


                transcription.textContent =
                    spokenText;


                setStatus(
                    "Transcription complete",
                    "Your spoken words were captured successfully."
                );


                setSystemStatus(
                    "TRANSCRIBED"
                );


                await processAgent(
                    spokenText
                );


            } catch (error) {

                console.error(
                    "[RECORDING]",
                    error
                );


                showError(
                    error.message
                );


                setStatus(
                    "Ready to listen",
                    "Press Start Recording to try again."
                );


                setSystemStatus(
                    "ERROR"
                );

            } finally {

                recording = false;

                processing = false;


                updateRecordButton();

                setRecordingVisual(
                    false
                );

            }

        }


        async function stopRecording() {

            if (!recording) {

                return;

            }


            recordButtonText.textContent =
                "Stopping...";


            setStatus(
                "Stopping recording...",
                "Finishing the current audio capture."
            );


            setSystemStatus(
                "STOPPING"
            );


            try {

                const serverResponse =
                    await fetch(
                        "/api/stop-recording",
                        {
                            method: "POST"
                        }
                    );


                const data =
                    await serverResponse.json();


                if (!serverResponse.ok) {

                    throw new Error(
                        data.error ||
                        "Unable to stop recording."
                    );

                }


            } catch (error) {

                console.error(
                    "[STOP RECORDING]",
                    error
                );

                showError(
                    error.message
                );

            }

        }


        async function processAgent(
            text
        ) {

            setStatus(
                "Thinking...",
                "Your selected AI agent is processing your request."
            );


            setSystemStatus(
                "PROCESSING"
            );


            try {

                const serverResponse =
                    await fetch(
                        "/api/run-agent",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({

                                    agent:
                                        agentSelect
                                            ? agentSelect.value
                                            : "Research",

                                    text:
                                        text

                                })
                        }
                    );


                const data =
                    await serverResponse.json();


                if (
                    !serverResponse.ok ||
                    !data.ok
                ) {

                    throw new Error(
                        data.error ||
                        "Agent processing failed."
                    );

                }


                response.textContent =
                    data.response || "";


                responsePanel.classList.remove(
                    "hidden"
                );


                setStatus(
                    "Response ready",
                    "Your agent has generated a response."
                );


                setSystemStatus(
                    "RESPONSE READY"
                );


                if (
                    voiceOutput &&
                    voiceOutput.checked &&
                    data.response
                ) {

                    await speakResponse(
                        data.response
                    );

                }


            } catch (error) {

                console.error(
                    "[AGENT]",
                    error
                );


                showError(
                    error.message
                );


                setStatus(
                    "Agent error",
                    "The agent could not process your request."
                );


                setSystemStatus(
                    "ERROR"
                );

            }

        }


        async function speakResponse(
            text
        ) {

            if (!text) {

                return;

            }


            if (speaking) {

                return;

            }


            speaking = true;


            updateSpeakButton();


            setStatus(
                "Speaking...",
                "The agent is reading the response aloud."
            );


            setSystemStatus(
                "SPEAKING"
            );


            try {

                const serverResponse =
                    await fetch(
                        "/api/speak",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    text: text
                                })
                        }
                    );


                const data =
                    await serverResponse.json();


                if (
                    !serverResponse.ok ||
                    !data.ok
                ) {

                    throw new Error(
                        data.error ||
                        "Speech failed."
                    );

                }


            } catch (error) {

                console.error(
                    "[TTS]",
                    error
                );


                showError(
                    error.message
                );

            } finally {

                speaking = false;


                updateSpeakButton();


                setStatus(
                    "Response ready",
                    "Press Speak Response to hear it again."
                );


                setSystemStatus(
                    "SYSTEM READY"
                );

            }

        }


        async function stopSpeaking() {

            if (!speaking) {

                return;

            }


            setStatus(
                "Stopping speech...",
                "Stopping the current voice output."
            );


            setSystemStatus(
                "STOPPING SPEECH"
            );


            try {

                const serverResponse =
                    await fetch(
                        "/api/stop-speaking",
                        {
                            method: "POST"
                        }
                    );


                if (!serverResponse.ok) {

                    throw new Error(
                        "Unable to stop speech."
                    );

                }


            } catch (error) {

                console.error(
                    "[STOP SPEECH]",
                    error
                );


                showError(
                    error.message
                );

            }


            speaking = false;


            updateSpeakButton();


            setStatus(
                "Response ready",
                "Press Speak Response to hear it again."
            );


            setSystemStatus(
                "SYSTEM READY"
            );

        }


        recordButton.addEventListener(
            "click",
            function () {

                if (recording) {

                    stopRecording();

                    return;

                }


                startRecording();

            }
        );


        if (speakButton) {

            speakButton.addEventListener(
                "click",
                function () {

                    if (speaking) {

                        stopSpeaking();

                        return;

                    }


                    const text =
                        response.textContent
                            .trim();


                    if (!text) {

                        showError(
                            "There is no response to speak."
                        );

                        return;

                    }


                    speakResponse(
                        text
                    );

                }
            );

        }


        if (clearButton) {

            clearButton.addEventListener(
                "click",
                async function () {

                    hideError();


                    if (recording) {

                        await stopRecording();

                    }


                    if (speaking) {

                        await stopSpeaking();

                    }


                    transcription.innerHTML =
                        '<span class="placeholder">' +
                        "Your spoken words will appear here..." +
                        "</span>";


                    response.textContent =
                        "";


                    responsePanel.classList.add(
                        "hidden"
                    );


                    setStatus(
                        "Ready to listen",
                        "Press Start Recording and speak naturally."
                    );


                    setSystemStatus(
                        "SYSTEM READY"
                    );

                }
            );

        }


        fetch(
            "/api/health"
        )
        .then(
            function (serverResponse) {

                return serverResponse.json();

            }
        )
        .then(
            function (data) {

                if (data.ok) {

                    setSystemStatus(
                        "SYSTEM READY"
                    );

                }

            }
        )
        .catch(
            function (error) {

                console.error(
                    "[HEALTH]",
                    error
                );


                setSystemStatus(
                    "SERVER OFFLINE"
                );

            }
        );

    }
);