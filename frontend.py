import streamlit as st
from utils.voice_agent import transcribe_audio, text_to_speech, process_voice_command
from orchestrator import run_agent

st.set_page_config(
    page_title="Voice-Controlled Agent System",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Voice-Controlled Agent System")
st.markdown("*Speak to AI agents and hear responses*")

# Sidebar
with st.sidebar:
    st.header("🎤 Voice Settings")
    duration = st.slider("Recording Duration (seconds)", 3, 10, 5)
    
    st.header("🤖 Agents")
    agent_choice = st.selectbox(
        "Select Agent",
        ["Research", "Summarizer"]
    )
    
    st.header("🔊 Voice Output")
    voice_output = st.checkbox("Enable Voice Output", value=True)
    
    st.header("ℹ️ How it works")
    st.write("""
    1. Click 'Start Recording'
    2. Speak your question
    3. AI transcribes and responds
    4. Hear the response aloud!
    """)

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    # Transcribed text display
    transcribed_text = st.text_area(
        "📝 Transcribed Text",
        height=100,
        placeholder="Your spoken words will appear here...",
        value=st.session_state.get("transcribed", "")
    )

with col2:
    st.write("")
    st.write("")
    if st.button("🎤 Start Recording", type="primary", use_container_width=True):
        with st.spinner(f"🎤 Recording for {duration} seconds..."):
            result = transcribe_audio(duration)
            st.session_state["transcribed"] = result
            
            if "Error" not in result:
                st.success("✅ Transcribed successfully!")
                
                # Process with agent
                with st.spinner("🧠 Processing with AI..."):
                    response = run_agent(agent_choice, result)
                    st.session_state["response"] = response
                    
                    # Display response
                    st.subheader("💬 Agent Response")
                    st.write(response)
                    
                    # Voice output
                    if voice_output and response:
                        st.info("🔊 Speaking response...")
                        text_to_speech(response[:500])
            else:
                st.error(result)

# Clear button
if st.button("🗑️ Clear"):
    st.session_state["transcribed"] = ""
    st.session_state["response"] = ""
    st.rerun()

st.caption("🎙️ Voice-Controlled Agent System | Powered by TinyLlama + Whisper")