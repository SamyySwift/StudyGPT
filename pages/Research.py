import streamlit as st
from streamlit_lottie import st_lottie
from utils.config import load_lottiefile
from streamlit_extras.add_vertical_space import add_vertical_space

col1, col2 = st.columns([2, 4])
with col1:
    lottie_bot = load_lottiefile("lotties/data-analysis.json")
    st_lottie(lottie_bot)

with col2:
    st.markdown("# :blue[Research]:red[Assistant]")
    st.markdown("**:blue[Extract relevant info from your documents]**")
    # st.markdown("#### Welcome! Samuel Okon👋")

add_vertical_space(2)

st.subheader("Upload files for indexing")
uploaded_file = st.file_uploader(
    ":blue[Upload your documents]", accept_multiple_files=True
)
st.button("Index Docs", key="index-btn")
add_vertical_space(3)
# Display a text input widget
st.text_input(
    ":blue[Search Documents]",
    key="main_query",
)

st.subheader("Registered Students")
data = {
    "Total Numbers": [
        12,
        20,
        15,
        8,
        30,
        17,
        22,
        10,
        14,
        18,
        25,
        9,
        16,
        19,
        13,
        21,
        27,
        11,
        23,
        28,
    ],
    "Department": [
        "Computer Science",
        "Law",
        "Engineering",
        "Business",
        "Medicine",
        "Psychology",
        "Design",
        "Education",
        "Marketing",
        "Physics",
        "Chemistry",
        "Biology",
        "Mathematics",
        "Sociology",
        "History",
        "English",
        "Geography",
        "Philosophy",
        "Economics",
        "Political Science",
    ],
    "Gender": [
        "M",
        "F",
        "M",
        "F",
        "M",
        "F",
        "M",
        "F",
        "M",
        "F",
        "M",
        "F",
        "M",
        "F",
        "M",
        "F",
        "M",
        "F",
        "M",
        "F",
    ],
    "Areas of Interest": [
        "Gaming, Tech, Health",
        "Tech, Movies",
        "Crpto, Music",
        "Sports, Travel",
        "Art, Photography",
        "Fashion, Food",
        "Writing, Literature",
        "Science, Research",
        "Environment, Sustainability",
        "Fitness, Nutrition",
        "Dance, Theater",
        "Politics, Law",
        "Music, History",
        "Film, TV",
        "Finance, Investing",
        "Technology, Gadgets",
        "Nature, Wildlife",
        "Psychology, Human Behavior",
        "Cooking, Baking",
        "Social Media, Influencer",
    ],
    "Age Range": [
        "18-20",
        "20-25",
        "19-23",
        "22-26",
        "24-28",
        "18-22",
        "20-24",
        "23-27",
        "25-29",
        "30-35",
        "26-30",
        "31-35",
        "35-40",
        "36-40",
        "40-45",
        "41-45",
        "45-50",
        "46-50",
        "50-55",
        "51-55",
    ],
}

st.table(data)
