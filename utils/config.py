from streamlit_custom_notification_box import custom_notification_box


notification_styles = {
    "material-icons": {"color": "white"},
    "text-icon-link-close-container": {"box-shadow": "#3896de 0px 4px"},
    "notification-text": {"": ""},
    "close-button": {"": ""},
    "link": {"": ""},
}


def display_alert(message, icon="info"):
    custom_notification_box(
        icon=icon,
        textDisplay=message,
        externalLink="",
        url="#",
        styles=notification_styles,
    )
