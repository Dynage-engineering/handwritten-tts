import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pytesseract
from gtts import gTTS
import os
from PIL import Image
import numpy as np


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

        st.write("Recognized text:", text)

        # Convert text to speech (TTS)
        if st.button("Convert to Speech"):
            tts(text)

    # Clear canvas button
    if st.button("Clear Canvas"):
        st.session_state.canvas_data = None
        st.rerun()


def tts(text):
    # Implement your TTS model here
    st.write("Converting to speech:", text)
    tts = gTTS(text)
    tts.save("output.mp3")
    st.audio("output.mp3")
