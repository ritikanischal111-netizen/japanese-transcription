import os

# ✅ FIX: Make ffmpeg visible to Whisper
os.environ["PATH"] += os.pathsep + "/usr/bin"

import streamlit as st
import whisper
import tempfile

st.title("Japanese Audio Transcription 🇯🇵")

uploaded_file = st.file_uploader(
    "Upload audio/video",
    type=["mp3", "wav", "m4a", "mp4"]
)

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    st.info("Transcribing... please wait ⏳")

    # Load Whisper model
    model = whisper.load_model("base")

    # Transcribe Japanese audio
    result = model.transcribe(temp_path, language="ja")

    st.subheader("Transcription")
    st.write(result["text"])

    # Clean up temp file
    os.remove(temp_path)
