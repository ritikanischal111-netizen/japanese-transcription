import streamlit as st
import whisper
import tempfile
import os

st.title("Japanese Audio Transcription")

uploaded_file = st.file_uploader("Upload audio/video", type=["mp3", "wav", "m4a", "mp4"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    model = whisper.load_model("base")
    result = model.transcribe(temp_path, language="ja")

    st.subheader("Transcription")
    st.write(result["text"])

    os.remove(temp_path)
