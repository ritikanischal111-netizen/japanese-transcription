import streamlit as st
import whisper
import tempfile
import os
import subprocess

# ================= DEV MODE (FOR YOU ONLY) =================
DEV_MODE = os.getenv("DEV_MODE") == "true"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Japanese Audio / Video Transcriber",
    page_icon="🎧",
    layout="centered"
)

st.title("🎧 Japanese Audio / Video Transcriber")

if DEV_MODE:
    st.success("🛠 Developer Mode Enabled — Unlimited Access")

# ================= FREE TRIAL INFO =================
st.info(
    "🎁 **Free Trial:** 2 audio/video uploads\n"
    "⏱️ **Max duration:** 3 minutes per file\n\n"
    "After the free trial, a subscription is required."
)

# ================= CONSTANTS =================
MAX_FREE_USES = 2
MAX_FREE_DURATION = 180  # seconds (3 minutes)

# ================= SESSION STATE =================
if "free_uses" not in st.session_state:
    st.session_state.free_uses = 0

remaining = max(0, MAX_FREE_USES - st.session_state.free_uses)

if not DEV_MODE:
    st.caption(f"🆓 Free uses remaining: {remaining}")
else:
    st.caption("♾ Unlimited usage (Developer)")

# ================= SUBSCRIPTION PLANS =================
st.markdown("---")
st.markdown("## 💳 Subscription Plans")
st.info("You can subscribe anytime. Payment is required only after the free trial ends.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ₹500 Basic")
    st.markdown("• Limited usage")
    st.markdown("• Small files")
    st.link_button("Subscribe ₹500", "https://rzp.io/rzp/mLuqttIf")

with col2:
    st.markdown("### ₹1000 Standard ⭐")
    st.markdown("• Medium usage")
    st.markdown("• Faster processing")
    st.link_button("Subscribe ₹1000", "https://rzp.io/rzp/3V33GQ1")

with col3:
    st.markdown("### ₹2000 Pro 🚀")
    st.markdown("• Unlimited usage")
    st.markdown("• Priority support")
    st.link_button("Subscribe ₹2000", "https://rzp.io/rzp/CkQNc0rq")

st.markdown("---")

# ================= LOAD WHISPER MODEL =================
@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader(
    "📤 Upload Audio or Video",
    type=["mp3", "wav", "m4a", "mp4"]
)

# ================= HELPERS =================
def get_audio_duration(file_path):
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

def block_if_exhausted():
    if not DEV_MODE:
        st.error("🚫 Free trial exhausted. Please subscribe to continue.")
        st.stop()

# ================= MAIN LOGIC =================
if uploaded_file:

    # 🚫 Block users only (not developer)
    if not DEV_MODE and st.session_state.free_uses >= MAX_FREE_USES:
        block_if_exhausted()

    if st.button("🚀 Transcribe"):

        with st.spinner("⏳ Processing your file..."):
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded_file.read())
                temp_path = tmp.name

            duration = get_audio_duration(temp_path)

            if duration is None:
                os.remove(temp_path)
                st.error("❌ Unable to read file duration.")
                st.stop()

            if not DEV_MODE and duration > MAX_FREE_DURATION:
                os.remove(temp_path)
                st.error("⏱️ Free trial supports files up to **3 minutes only**.")
                block_if_exhausted()

            # 🔊 TRANSCRIBE
            result = model.transcribe(temp_path, language="ja")
            os.remove(temp_path)

        # ✅ SUCCESS
        if not DEV_MODE:
            st.session_state.free_uses += 1
            remaining = max(0, MAX_FREE_USES - st.session_state.free_uses)

        st.success("✅ Transcription completed!")

        st.markdown("### 📄 Transcription Result")
        st.text_area("Japanese Text", result["text"], height=300)

        st.download_button(
            "⬇️ Download Transcript",
            data=result["text"],
            file_name="transcription.txt",
            mime="text/plain"
        )

        if not DEV_MODE:
            if remaining > 0:
                st.success(f"🎉 {remaining} free transcription(s) remaining.")
            else:
                st.warning("⚠️ Free trial completed. Please subscribe for continued access.")
