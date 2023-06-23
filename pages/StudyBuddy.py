import streamlit as st
from utils.config import display_animation
from streamlit_extras.add_vertical_space import add_vertical_space
from FlipBot import Message

col1, col2 = st.columns([2, 4])
with col1:
    display_animation("lotties/buddies.json")

with col2:
    st.markdown("# :blue[Study]:red[Buddy]")
    st.markdown("**:blue[Meet your study partner]**")


st.markdown(
    ":green[Yaay!!!!]🎉:blue[Flip]:red[Bot] mactched 🧑‍🤝‍🧑you both😁. You can help each other learn this course effectively😉"
)

add_vertical_space(2)

st.subheader("Share Files")
uploaded_file = st.file_uploader(
    ":blue[share files with your buddy]", accept_multiple_files=True
)

chat_placeholder = st.container()

with chat_placeholder:
    for chat in st.session_state.history:
        div = f"""
        <div class="chat-row 
                    {'' if chat.origin == 'ai' else 'row-reverse'}">
                    <img class="chat-icon" src="app/static/{
                        'ai_icon.png' if chat.origin == 'ai' 
                                    else 'user.png'}"
                        width=32 height=32>
                <div class="chat-bubble
                    {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
                        &#8203;{chat.message}
                </div>
        </div>
                    """
        st.markdown(div, unsafe_allow_html=True)

        # Display a text input widget

add_vertical_space(2)
st.text_input(
    ":blue[Ask FlipBot any question as well as follow up questions]",
    placeholder="Ask questions based on your uploaded materials...",
    # on_change=clear_main_query,
    key="main_query",
)
