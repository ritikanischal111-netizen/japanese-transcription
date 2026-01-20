import tempfile
import os
import whisper
import streamlit as st

model = whisper.load_model("base")

uploaded_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a", "mp4"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    st.write("Transcribing... ⏳")
    result = model.transcribe(temp_path, language="ja")
    st.text(result["text"])

    os.remove(temp_path)
