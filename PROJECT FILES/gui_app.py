import streamlit as st
import asyncio
import edge_tts
import os
import joblib
from io import BytesIO
from sentence_transformers import SentenceTransformer
from deep_translator import GoogleTranslator

# Load model and encoder
model = joblib.load("genre_classifier_cleaned.pkl")
mlb = joblib.load("label_binarizer_cleaned.pkl")
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Voice and language mapping
voice_map = {
    "English": ("en", "en-US-AriaNeural"),
    "Urdu": ("ur", "ur-PK-AsadNeural"),
    "Arabic": ("ar", "ar-SA-HamedNeural"),
    "Korean": ("ko", "ko-KR-SunHiNeural")
}

# Setup
st.set_page_config(page_title="🎬 Movie Summary AI", layout="centered")
st.title("🎥 Movie Summary Analyzer")
st.markdown("Paste a movie summary, and choose an action below.")

summary = st.text_area("✍ Enter Movie Summary", height=200, placeholder="e.g. A young man moves to the city...")

# Reset input
if st.button("🔄 Clear Input"):
    st.experimental_rerun()

option = st.radio("Choose Action:", ["Convert Summary to Audio", "Predict Genre"])

# Translation + Audio
def translate_text(text, lang_code):
    return GoogleTranslator(source='auto', target=lang_code).translate(text)

async def generate_audio(text, voice):
    output_file = "AI Generated Work/audio_output.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

# Create folder
def ensure_folder():
    folder = "AI Generated Work"
    os.makedirs(folder, exist_ok=True)
    return folder

# AUDIO FLOW
if option == "Convert Summary to Audio" and summary:
    language = st.selectbox("🌍 Select Language", list(voice_map.keys()))
    if st.button("🔊 Translate & Generate Audio"):
        try:
            lang_code, voice = voice_map[language]
            translated = translate_text(summary, lang_code)
            st.text_area("📝 Translated Text", translated, height=100)

            st.info("⏳ Generating audio...")
            asyncio.run(generate_audio(translated, voice))

            audio_path = "AI Generated Work/audio_output.mp3"
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            st.success("✅ Audio Generated!")
            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                label="💾 Download Audio File",
                data=audio_bytes,
                file_name="audio_summary.mp3",
                mime="audio/mpeg"
            )
        except Exception as e:
            st.error(f"❌ Error: {e}")

# GENRE PREDICTION
elif option == "Predict Genre" and summary:
    if st.button("🎯 Predict Genre"):
        try:
            embedding = encoder.encode([summary])
            pred_probs = model.predict_proba(embedding)[0]
            top_indices = pred_probs.argsort()[-3:][::-1]
            top_genres = [mlb.classes_[i] for i in top_indices if pred_probs[i] > 0.2]

            if top_genres:
                st.success("🎬 Top 3 Predicted Genres:")
                genre_text = ""
                for genre in top_genres:
                    st.markdown(f"- {genre}")
                    genre_text += f"{genre}\n"

                folder = ensure_folder()
                genre_path = os.path.join(folder, "genre_prediction.txt")
                with open(genre_path, "w", encoding="utf-8") as f:
                    f.write(genre_text)

                st.download_button(
                    label="💾 Download Genre Prediction",
                    data=genre_text,
                    file_name="genre_prediction.txt",
                    mime="text/plain"
                )
            else:
                st.warning("🤔 No genre could be confidently predicted.")
        except Exception as e:
            st.error(f"❌ Genre Prediction Error: {e}")