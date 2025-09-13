import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests

# ---- Lottie Animation Loader ----
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# ---- Page Theme & Style ----
st.set_page_config(
    page_title="💧 Hydration Playground",
    page_icon="💧",
    layout="wide"
)

st.markdown("""
<style>
body {background: linear-gradient(to top right, #13f1fc, #0470dc);}
.hydro-bubble {
    background: rgba(255,255,255,0.44);
    border-radius: 22px;
    box-shadow: 0 4px 24px 0 rgba(31,38,135,0.17);
    color: #22337a;
    padding: 30px 18px;
    font-size: 1.15em;
    margin: 22px 0;
    position: relative;
}
.st-emotion-cache-1m18cay {
    background: linear-gradient(135deg, #80ffea 40%, #f067b4 100%) !important;
}
</style>
""", unsafe_allow_html=True)

# ---- Hydration Goal & Reminder ----
st.sidebar.header("✨ Settings & Reminders")
goal_liters = st.sidebar.slider("🚀 Set Daily Hydration Goal", 2.0, 5.0, 3.0, 0.1)
st.sidebar.markdown(f'<div class="hydro-bubble">Goal: <b>{goal_liters}L</b> 💧</div>', unsafe_allow_html=True)

units = st.sidebar.radio("Pick reminder unit", ["Hour(s)", "Minute(s)"], horizontal=True)
value = st.sidebar.number_input("Custom reminder every:", min_value=1, max_value=480, step=1)
if st.sidebar.button("🔔 Set Reminder"):
    t_unit = "minute" if units == "Minute(s)" else "hour"
    st.sidebar.success(f"🎉 Reminder set for every {value} {t_unit}(s)! Hydrate like a hero!")

# ---- Lottie Animation Banner ----
st.markdown("<h1 style='text-align: center; font-size:3em; color:#0470dc;'>Water Intake Tracker 💧</h1>", unsafe_allow_html=True)
lottie_water = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")
if lottie_water:
    from streamlit_lottie import st_lottie
    st_lottie(lottie_water, speed=1, height=130, key="waterAnim")

# ---- Data Storage ----
today = datetime.date.today()
if "water_data" not in st.session_state:
    st.session_state["water_data"] = {}

water_data = st.session_state["water_data"]

# ---- User Input ----
todays_input = st.number_input("💦 Enter today's water intake (L):", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
if st.button("🚰 Save Today's Intake"):
    water_data[today.strftime("%Y-%m-%d")] = todays_input
    st.session_state["water_data"] = water_data  # sync
    st.balloons()
    st.success("Intake saved! Hydration FTW. 🤩")

# ---- Prepare Hydration History ----
dates = [today - datetime.timedelta(days=i) for i in range(6, -1, -1)]
intake_history = [water_data.get(d.strftime("%Y-%m-%d"), np.nan) for d in dates]
intake_history = [0 if np.isnan(x) else x for x in intake_history]
df_week = pd.DataFrame({'Date': [d.strftime("%a %d %b") for d in dates], 'Intake (L)': intake_history})

# ---- Rainbow Progress Bar ----
progress = min(intake_history[-1] / goal_liters, 1.0)
progress_perc = int(progress * 100)
st.markdown(f"""
<div class='hydro-bubble'>
    <b>Today's Progress:</b><br>
    <div style='background: linear-gradient(90deg, #13f1fc, #fc2b83, #fdbb2d); 
                border-radius:16px; height:28px; width:{max(progress_perc,10)}%; 
                text-align:center; color:#22337a; font-size:1.4em;'>
        {progress_perc}%
    </div>
    <br><span style="font-size:1.1em">Drank: <b>{intake_history[-1]:.2f}L</b> / <b>{goal_liters:.2f}L</b></span>
    {"🎉" if progress_perc == 100 else "✨"}
</div>
""", unsafe_allow_html=True)

# ---- Weekly Chart ----
st.markdown("<h2 style='color:#f067b4;'>Weekly Hydration Chart 🌈</h2>", unsafe_allow_html=True)
st.bar_chart(df_week.set_index('Date'), use_container_width=True, color="#13f1fc")

# ---- Comic Bubbles ----
st.markdown("<h3 style='color:#22c1c3;'>Comic Bubbles: Last 7 Days</h3>", unsafe_allow_html=True)
cols = st.columns(7)
for i, col in enumerate(cols):
    water_amt = intake_history[i]
    bubble = f"""<div class='hydro-bubble' style='background:rgba(240,103,180,0.24);'>
        <b>{df_week['Date'][i]}</b><br/>
        <span style='font-size:1.45em;'>{'🟦'*int(water_amt*2)}</span><br/>
        <span>{water_amt:.2f}L</span>
    </div>"""
    col.markdown(bubble, unsafe_allow_html=True)
