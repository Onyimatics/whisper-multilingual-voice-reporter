# streamlit_app.py (Enhanced with playback + language name + English TTS)

import streamlit as st
import whisper
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import tempfile
import os
from gtts.lang import tts_langs
from IPython.display import Audio

# Helper to convert short language codes to full names
LANGUAGES = {
    'af': 'Afrikaans', 'ar': 'Arabic', 'bn': 'Bengali', 'bg': 'Bulgarian', 'zh': 'Chinese',
    'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'fi': 'Finnish',
    'fr': 'French', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'hi': 'Hindi',
    'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'kn': 'Kannada',
    'ko': 'Korean', 'ml': 'Malayalam', 'mr': 'Marathi', 'ne': 'Nepali', 'no': 'Norwegian',
    'pa': 'Punjabi', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian',
    'sr': 'Serbian', 'es': 'Spanish', 'sv': 'Swedish', 'ta': 'Tamil', 'te': 'Telugu',
    'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese'
}

st.set_page_config(page_title="🌍 Multilingual Civic Voice Reporter", layout="centered")
st.title("🗣️ Multilingual Voice Reporter")
st.markdown("Upload a voice note in **any language**, and receive a spoken response in the same language.")

# Upload voice note
uploaded_file = st.file_uploader("🎧 Upload your voice file (mp3 or wav)", type=["mp3", "wav"])

if uploaded_file:
    # Display uploaded audio
    st.audio(uploaded_file, format="audio/mp3")
    st.info("🧠 Loading model and processing...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    # Load Whisper and transcribe
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio_path)
    detected_lang = result["language"]
    user_text = result["text"]

    lang_full = LANGUAGES.get(detected_lang, detected_lang.upper())

    st.success(f"🌐 Detected Language: {lang_full}")
    st.markdown(f"**📝 Transcription:** {user_text}")

    # Translate to English
    translator = Translator()
    english_translation = translator.translate(user_text, src=detected_lang, dest='en').text
    st.markdown(f"**🌍 English Translation:** {english_translation}")

    # Simulate English response
    english_reply = "Thank you. Your report has been received. The appropriate team will respond shortly."
    st.markdown(f"**📣 English Response:** {english_reply}")

    # Generate English TTS
    tts_en = gTTS(text=english_reply, lang='en')
    en_path = os.path.join(tempfile.gettempdir(), "response_en.mp3")
    tts_en.save(en_path)
    st.audio(en_path, format="audio/mp3")

    # Translate English reply back to user's language
    if detected_lang in tts_langs():
        user_reply = translator.translate(english_reply, src='en', dest=detected_lang).text
        st.markdown(f"**🔁 Reply in {lang_full}:** {user_reply}")

        # Generate reply in user's language
        tts = gTTS(text=user_reply, lang=detected_lang)
        user_path = os.path.join(tempfile.gettempdir(), "response_user.mp3")
        tts.save(user_path)

        st.info("🎙️ Synthesizing reply...")
        st.audio(user_path, format="audio/mp3")
        st.success("✅ Voice response complete!")
    else:
        st.error(f"Sorry, text-to-speech not supported for language: {lang_full}")
