import streamlit as st
import whisper
import tempfile
import os
import subprocess

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Japanese Audio / Video Transcriber",
    page_icon="🎧",
    layout="centered"
)

st.title("🎧 Japanese Audio / Video Transcriber")

st.info(
    "🎁 **Free Trial:** 2 audio/video uploads (up to **3 minutes each**).\n\n"
    "After the free trial, a subscription is required."
)

# ---------------- SESSION STATE ----------------
if "free_uses" not in st.session_state:
    st.session_state.free_uses = 0

MAX_FREE_USES = 2
MAX_FREE_DURATION = 180  # seconds (3 minutes)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

# ---------------- SHOW FREE USES LEFT ----------------
remaining = MAX_FREE_USES - st.session_state.free_uses
st.caption(f"🆓 Free uses remaining: {remaining if remaining > 0 else 0}")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📤 Upload Audio or Video",
    type=["mp3", "wav", "m4a", "mp4"]
)

# ---------------- FUNCTIONS ----------------
def get_audio_duration(file_path):
    """Get duration using ffprobe (works on Streamlit Cloud)"""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return float(result.stdout.strip())
    except Exception:
        return None

def show_pricing():
    st.markdown("---")
    st.subheader("🔓 Unlock Full Access")

    st.write("Your free trial is over. Please subscribe to continue.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🟢 Basic – ₹500")
        st.write("Up to **10 MB** audio/video")
        st.markdown("[👉 Subscribe Now](https://rzp.io/rzp/mLuqttIf)")

    with col2:
        st.markdown("### 🔵 Standard – ₹1000")
        st.write("**10–50 MB** audio/video")
        st.markdown("[👉 Subscribe Now](https://rzp.io/rzp/3V33GQ1)")

    with col3:
        st.markdown("### 🔴 Pro – ₹2000")
        st.write("**Above 50 MB** audio/video")
        st.markdown("[👉 Subscribe Now](https://rzp.io/rzp/CkQNc0rq)")

# ---------------- MAIN LOGIC ----------------
if uploaded_file:

    if st.session_state.free_uses >= MAX_FREE_USES:
        st.error("🚫 Free trial exhausted.")
        show_pricing()
        st.stop()

    if st.button("🚀 Transcribe"):

        with st.spinner("⏳ Processing your file..."):

            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded_file.read())
                temp_path = tmp.name

            duration = get_audio_duration(temp_path)

            if duration is None:
                os.remove(temp_path)
                st.error("❌ Could not read file duration.")
                st.stop()

            if duration > MAX_FREE_DURATION:
                os.remove(temp_path)
                st.error("⏱️ Free trial supports files up to **3 minutes only**.")
                show_pricing()
                st.stop()

            # ---------------- TRANSCRIPTION ----------------
            result = model.transcribe(temp_path, language="ja")
            os.remove(temp_path)

        # ---------------- SUCCESS ----------------
        st.session_state.free_uses += 1
        remaining = MAX_FREE_USES - st.session_state.free_uses

        st.success("✅ Transcription completed!")

        st.markdown("### 📄 Transcription Result")
        st.text_area(
            "Japanese Text",
            result["text"],
            height=300
        )

        st.download_button(
            "⬇️ Download Transcript",
            data=result["text"],
            file_name="transcription.txt",
            mime="text/plain"
        )

        if remaining > 0:
            st.success(f"🎉 {remaining} free transcription(s) remaining.")
        else:
            st.warning("⚠️ This was your last free trial.")
            show_pricing()
