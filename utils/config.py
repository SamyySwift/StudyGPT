from streamlit_custom_notification_box import custom_notification_box
import streamlit as st
from streamlit_card import card
import json


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
        image="https://firebasestorage.googleapis.com/v0/b/flipbot-4f922.appspot.com/o/WhatsApp%20Image%202023-06-22%20at%209.25.18%20AM.jpeg?alt=media&token=031d8a01-5aad-4c23-b296-220fa7c8df84",
        url="https://www.google.com",
    )
