import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Japanese Transcription Tool")
st.title("🎧 Japanese Audio / Video Transcriber")

@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

uploaded_file = st.file_uploader(
    "Upload Audio or Video",
    type=["mp3", "wav", "m4a", "mp4"]
)

if uploaded_file:
    if st.button("Transcribe"):
        with st.spinner("Please wait..."):
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded_file.read())
                temp_path = tmp.name

            result = model.transcribe(temp_path, language="ja")
            os.remove(temp_path)

        st.success("Done!")
        st.text_area("Transcription", result["text"], height=300)
