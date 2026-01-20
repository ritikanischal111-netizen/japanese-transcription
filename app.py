import os
import tempfile
import streamlit as st
import whisper

# Make ffmpeg visible
os.environ["PATH"] += os.pathsep + "/usr/bin"

# ---------------- CONFIG ----------------
FREE_TRIAL_SECONDS = 240  # 4 minutes

PAYMENT_LINK_1 = "https://rzp.io/l/your-basic-plan"
PAYMENT_LINK_2 = "https://rzp.io/l/your-pro-plan"

# ---------------- PAGE UI ----------------
st.set_page_config(
    page_title="Japanese Audio Transcription",
    page_icon="🇯🇵",
    layout="centered"
)

st.title("🇯🇵 Japanese Audio & Video Transcription")
st.caption("Fast • Accurate • Whisper-powered")

st.markdown("---")

# ---------------- UPLOAD ----------------
st.subheader("📤 Upload your audio/video")

uploaded_file = st.file_uploader(
    "Supported formats: MP3, WAV, M4A, MP4",
    type=["mp3", "wav", "m4a", "mp4"]
)

# ---------------- BUTTON ----------------
transcribe_clicked = st.button("🚀 Transcribe Now")

# ---------------- LOGIC ----------------
if uploaded_file and transcribe_clicked:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    with st.spinner("🔍 Analyzing audio duration..."):
        model = whisper.load_model("base")
        audio = whisper.load_audio(temp_path)
        duration = len(audio) / 16000  # seconds

    st.info(f"⏱ Audio length: {int(duration)} seconds")

    # ---------- FREE TRIAL ----------
    if duration <= FREE_TRIAL_SECONDS:
        st.success("🎉 Free trial applied (up to 4 minutes)")

        with st.spinner("🧠 Transcribing..."):
            result = model.transcribe(temp_path, language="ja")

        st.subheader("📄 Transcription Result")
        st.text_area(
            "Text",
            result["text"],
            height=200
        )

        st.download_button(
            "⬇ Download Transcript",
            result["text"],
            file_name="transcription.txt"
        )

    # ---------- PAYMENT REQUIRED ----------
    else:
        st.warning("⚠ Audio longer than free limit")

        st.markdown("### 🔐 Choose a plan to continue")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Basic Plan**")
            st.markdown("✔ Up to 30 minutes")
            st.link_button("Pay ₹99", PAYMENT_LINK_1)

        with col2:
            st.markdown("**Pro Plan**")
            st.markdown("✔ Unlimited usage")
            st.link_button("Pay ₹299", PAYMENT_LINK_2)

        st.info(
            "After payment, return here and re-upload the file.\n"
            "Auto-verification can be added next."
        )

    os.remove(temp_path)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with ❤️ using OpenAI Whisper & Streamlit")
