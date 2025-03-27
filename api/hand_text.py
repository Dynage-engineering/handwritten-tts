import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pytesseract
from gtts import gTTS
import gtts
import os
from PIL import Image
import numpy as np
from api.voice_clone import voice_clone_with_resemble


def get_hand_text_from_canvas():

    # Initialize session state for canvas
    if "canvas_data" not in st.session_state:
        st.session_state.canvas_data = None

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=2,
        stroke_color="#000000",
        background_color="#ffffff",
        height=300,
        width=600,
        drawing_mode="freedraw",
        key="canvas",
        update_streamlit=True,
    )

    # Process the canvas image
    if canvas_result.image_data is not None:
        st.session_state.canvas_data = canvas_result.image_data
        img = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")
        img = img.convert("L")  # Convert to grayscale
        img = np.array(img)

        # Use pytesseract to extract text
        text = pytesseract.image_to_string(img)
        languages = gtts.lang.tts_langs()
        language = st.selectbox("Select language", list(languages.values()))
        st.write("Selected language:", language)
        st.write("Recognized text:", text)

        # use custom voice cloning model to convert text to speech
        # st.button(
        #     "Use custom voice",
        #     type="primary",
        #     on_click=voice_clone_with_resemble,
        #     args=(text, language),
        # )
        audio_value = st.audio_input("Record a voice message")
        print(f"audio_value: {audio_value}")
        if audio_value:
            st.audio(audio_value)
            print(f"audio_value: {audio_value}")
        output = voice_clone_with_resemble(audio_value, text)
        print(f"output:{output}")
        st.audio(output)

        # Convert text to speech (TTS)
        if st.button("Convert to Speech"):
            language = select_language(language, languages)
            tts(text, language)


def select_language(language, languages):
    for key, value in languages.items():
        if value == language:
            return key


def tts(text, language):
    # Implement your TTS model here
    st.write("Converting to speech:", text)
    tts = gTTS(text, lang=language)
    tts.save("output.mp3")
    st.audio("output.mp3")
