import streamlit as st

from api.hand_text import get_hand_text_from_canvas


def createUI():
    st.title("Hand-Written-Text-To-Speech")
    st.text(
        "Draw a character in the canvas below and click 'Convert to Speech' to hear the audio output."
    )
    get_hand_text_from_canvas()
