import streamlit as st

# Page configuration for professional, minimal look
st.set_page_config(
    page_title="Quiz Game App",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom style adjustments for clarity and focus
st.markdown(
    """
    <style>
        .main {background-color: #F9F9FB;}
        .stRadio label, .stButton button {
            font-weight: 500;
        }
        .score-box {
            background-color: #eaf4ff;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
            font-size: 1.4rem;
            color: #3376c0;
            margin-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Hardcoded quiz questions
QUESTIONS = [
    {
        "question": "Which language is used for web apps?",
        "options": ["PHP", "Python", "JavaScript", "All of the above"],
        "answer": "All of the above"
    },
    {
        "question": "Who developed the Python language?",
        "options": ["Zim Den", "Guido van Rossum", "Niene Stom", "Wick van Rossum"],
        "answer": "Guido van Rossum"
    },
    {
        "question": "What year was Streamlit launched?",
        "options": ["2016", "2018", "2019", "2021"],
        "answer": "2019"
    }
]

# Initialize session state for score and progress
if "question_idx" not in st.session_state:
    st.session_state.question_idx = 0
    st.session_state.score = 0
    st.session_state.selected = None
    st.session_state.finished = False

def reset_quiz():
    st.session_state.question_idx = 0
    st.session_state.score = 0
    st.session_state.selected = None
    st.session_state.finished = False

st.title("❓ Quiz Game App")

# Progress bar at top for professionalism
progress = (st.session_state.question_idx) / len(QUESTIONS)
st.progress(progress)

# Quiz Logic
if not st.session_state.finished:
    idx = st.session_state.question_idx
    question = QUESTIONS[idx]

    st.subheader(f"Question {idx + 1} of {len(QUESTIONS)}")
    user_answer = st.radio(
        question["question"],
        question["options"],
        index=None,
        key=f"answer_{idx}"
    )

    if user_answer is not None:
        st.session_state.selected = user_answer

    # Next button logic
    if st.button("Next", disabled=st.session_state.selected is None):
        if st.session_state.selected == question["answer"]:
            st.session_state.score += 1
        st.session_state.question_idx += 1
        st.session_state.selected = None
        if st.session_state.question_idx >= len(QUESTIONS):
            st.session_state.finished = True

# Final score display
if st.session_state.finished:
    st.markdown(
        f'<div class="score-box">Your final score: <strong>{st.session_state.score} / {len(QUESTIONS)}</strong></div>',
        unsafe_allow_html=True
    )
    st.button("Restart Quiz", on_click=reset_quiz)
