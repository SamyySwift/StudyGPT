from streamlit_custom_notification_box import custom_notification_box
import streamlit as st
from streamlit_card import card
import json
from streamlit_lottie import st_lottie

notification_styles = {
    "material-icons": {"color": "white"},
    "text-icon-link-close-container": {"box-shadow": "#3896de 0px 4px"},
    "notification-text": {"": ""},
    "close-button": {"": ""},
    "link": {"": ""},
}


@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)


def display_animation(path):
    lottie_bot = load_lottiefile(path)
    st_lottie(lottie_bot)


def display_alert(message, icon="info"):
    custom_notification_box(
        icon=icon,
        textDisplay=message,
        externalLink="",
        url="#",
        styles=notification_styles,
    )


def matching_notification():
    card(
        title="Matching Alert",
        text="Some other user uploaded this exact document, would you like to study together?",
        image="https://firebasestorage.googleapis.com/v0/b/flipbot-4f922.appspot.com/o/logo.jpeg?alt=media&token=1b8a2ccf-11c8-49a8-bd20-4de1ed6e1f69",
        url="https://flipbot.streamlit.app/StudyBuddy",
    )
