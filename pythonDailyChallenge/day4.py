import streamlit as st
import numpy as np

st.set_page_config(
    page_title="BMI Playground 🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏋️"
)

# Inject some wild CSS for a glassy, comic, rainbow look
st.markdown("""
    <style>
        body {
            background: linear-gradient(120deg,#f72585 30%,#7209b7 60%, #3a86ff 100%) fixed;
        }
        .stApp {
            font-family: 'Comic Sans MS', 'Comic Neue', cursive;
        }
        .bmi-result {
            border-radius: 28px;
            background: linear-gradient(120deg,#ffbe0b 5%,#fb5607 55%,#ff006e 100%);
            box-shadow: 0 8px 40px 0 rgba(0,0,0,0.38);
            color: white;
            padding: 30px 50px;
            text-align: center;
            font-size: 2.2rem;
            margin-top: 12px;
            margin-bottom: 8px;
            animation: bounce 1.2s ;
        }
        @keyframes bounce {
            0% {transform: scale(0.7);}
            60% {transform: scale(1.1);}
            80% {transform: scale(0.98);}
            100% {transform: scale(1);}
        }
        .category-chip {
            display: inline-block;
            background: rgba(224,255,0,0.8);
            border-radius: 100px;
            padding: 18px 40px;
            font-weight: bold;
            font-size: 1.7rem;
            color: #7209b7;
            margin: 25px auto;
            box-shadow: 0 2px 18px rgba(250,250,0,0.5);
            border: 2px solid #f72585;
            animation: jiggle .8s infinite alternate;
        }
        @keyframes jiggle {
            0% { transform: rotate(-1deg);}
            100% { transform: rotate(1deg);}
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎨 BMI Calculator Playground 🏋️")
st.write("Enter your *height* and *weight*—get instant results with wild colors & emojis!")

col1, col2, col3 = st.columns([2,2,2])
with col1:
    st.image("https://em-content.zobj.net/thumbs/240/apple/354/trophy_1f3c6.png", width=100)
with col2:
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0,
        step=0.1, help="How tall? Stand proud like a statue!")
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, value=70.0,
        step=0.1, help="How heavy? Add a pizza if you wish!")

with col3:
    st.image("https://em-content.zobj.net/thumbs/240/apple/354/party-popper_1f389.png", width=100)

if st.button("💥 Calculate my BMI!"):
    m_height = height / 100
    bmi = np.round(weight / (m_height**2), 2)
    if bmi < 18.5:
        category, emoji = "Underweight", "🦴😅"
        chip_color = "#ffc300"
    elif 18.5 <= bmi < 25:
        category, emoji = "Normal", "🦸🏻‍♂️💪"
        chip_color = "#4bb543"
    elif 25 <= bmi < 30:
        category, emoji = "Overweight", "🎈😏"
        chip_color = "#ff9800"
    else:
        category, emoji = "Obese", "🔴😮"
        chip_color = "#f72585"

    st.markdown(f'<div class="bmi-result"> '
                f'Your <b>BMI</b>: <span style="font-size:2.8rem; text-shadow:0 6px 14px #fff;">{bmi}</span> '
                f' </div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="category-chip" style="background:{chip_color};"> '
        f'{emoji} <b>{category}</b> {emoji} </div>',
        unsafe_allow_html=True
    )

    st.write("BMI = Weight(kg) / [Height(m)]²")
    st.info("Ready, set, glow! See where you land – then party or power up! 🎉")
else:
    st.write("👟 Drop your numbers and smash the giant button! 🚀")

st.markdown("----")
st.write("**Categories:**")
st.markdown("""
- Underweight: BMI < 18.5  
- Normal: BMI 18.5–24.9  
- Overweight: BMI 25–29.9  
- Obese: BMI ≥ 30  
""")

st.success("This playful app makes healthy tracking feel like a game—add more confetti, sound, or animations to surprise demo crowds! 🌈")
