import streamlit as st
import requests
from streamlit_lottie import st_lottie

# ==== Playground theming ====
st.set_page_config(page_title="Unit Converter Playground 🔄", layout="centered", page_icon="🔄")
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background: linear-gradient(130deg, #fdffb6, #bdb2ff, #ffadad, #9bf6ff) fixed !important;
        }
        h1, h3, .stTabs [role=tab] {
            font-family: 'Comic Sans MS', cursive;
            color: #22223b !important;
            text-shadow: 2px 2px 6px #80ffdb;
        }
        .bubble {
            background: rgba(255,255,255,0.98);
            color: #ff2992;
            border-radius: 1.6em 1.3em 1.5em 0.7em;
            display: inline-block;
            padding: 1.3em 1.8em;
            font-weight: bold;
            font-size: 2em;
            border: 4px solid #9bf6ff;
            margin-top: 1.5em;
            animation: pop 0.8s;
        }
        @keyframes pop {
            0% {transform: scale(0.6);}
            80% {transform: scale(1.08);}
            100% {transform: scale(1);}
        }
        div.stButton button {
            background-image: linear-gradient(92deg,#ff0054,#7afcff,#fdffb6,#ff0054);
            background-size: 400% 100%;
            animation: rainbow 2.5s linear infinite;
            color: #131313;
            font-size: 1.2em;
            padding: 0.5em 2em;
            border-radius: 1.5em;
            border: none;
        }
        @keyframes rainbow {
            0% {background-position: 0%;}
            100% {background-position: 100%;}
        }
    </style>
""", unsafe_allow_html=True)

# --- Playful safe Lottie loader ---
def load_lottie_url(url):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None

# Lottie URLs (all public, vibrant!)
ANIMS = {
    "coin": "https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json",
    "rocket": "https://assets10.lottiefiles.com/packages/lf20_hgjazwls.json",
    "ruler": "https://assets4.lottiefiles.com/packages/lf20_puciaact.json",  # rainbow ruler
    "weight": "https://assets6.lottiefiles.com/private_files/lf30_maqwrcyb.json",  # barbell
    "fallback": "https://assets4.lottiefiles.com/packages/lf20_u4yrau.json"  # smile emoji
}

def fun_anim(key):
    anim = load_lottie_url(ANIMS.get(key, ANIMS["fallback"]))
    if anim:
        st_lottie(anim, height=80, key=key)
    else:
        st_lottie(load_lottie_url(ANIMS["fallback"]), height=70, key=f"{key}_fallback")

st.markdown("<h1 style='text-align:center;'>Unit Converter Playground 🎉🔄🦄</h1>", unsafe_allow_html=True)
tabs = st.tabs(["💸 Currency", "🌡️ Temp", "📏 Length", "🏋️ Weight"])

# --- Currency ---
with tabs[0]:
    fun_anim("coin")
    st.subheader("Neon Currency Converter")
    currs = ['USD','EUR','INR','GBP','JPY','AUD','CAD','SGD']
    fr_cur = st.selectbox("From", currs, index=0)
    to_cur = st.selectbox("To", currs, index=2)
    amt = st.slider("Amount", 1.0, 10000.0, 99.0, step=1.0, format="%.2f")
    if st.button("💸 Convert! 💸"):
        url = f"https://api.exchangerate-api.com/v4/latest/{fr_cur}"
        try:
            r = requests.get(url, timeout=5)
            data = r.json()
            rate = data["rates"][to_cur]
            result = amt * rate
            st.markdown(f"<div class='bubble'>{amt:.2f} {fr_cur} = {result:.2f} {to_cur} 🎉</div>", unsafe_allow_html=True)
        except Exception:
            st.markdown(f"<div class='bubble'>🌈 Oops! Couldn’t fetch rates, but you still sparkle!</div>", unsafe_allow_html=True)

# --- Temperature ---
with tabs[1]:
    fun_anim("rocket")
    st.subheader("Explosive Temp Converter")
    units = ["Celsius","Fahrenheit","Kelvin"]
    fr_temp = st.selectbox("Convert from", units)
    to_temp = st.selectbox("Convert to", units, index=1)
    tv = st.slider("Temperature", -100.0, 300.0, 25.0, format="%.1f")
    if st.button("🔥 Blast! 🚀"):
        def tconv(v,f,t):
            if f==t: return v
            tf = {
                ("Celsius","Fahrenheit"): lambda c: (c*9/5)+32,
                ("Celsius","Kelvin"): lambda c: c+273.15,
                ("Fahrenheit","Celsius"): lambda f: (f-32)*5/9,
                ("Fahrenheit","Kelvin"): lambda f: (f-32)*5/9+273.15,
                ("Kelvin","Celsius"): lambda k: k-273.15,
                ("Kelvin","Fahrenheit"): lambda k: (k-273.15)*9/5+32,
            }
            return tf.get((f,t), lambda x: x)(v)
        cool = tconv(tv, fr_temp, to_temp)
        emoji = "💥" if (fr_temp=="Celsius" and cool>100) else "❄️" if cool<0 else "🌞"
        st.markdown(f"<div class='bubble'>{tv}° {fr_temp} = {cool:.2f}° {to_temp} {emoji}</div>", unsafe_allow_html=True)

# --- Length ---
with tabs[2]:
    fun_anim("ruler")
    st.subheader("Stretchy Length Converter")
    ln = ["Meters","Kilometers","Miles","Feet","Inches","Centimeters"]
    f_ln = st.selectbox("From", ln)
    t_ln = st.selectbox("To", ln, index=3)
    n_ln = st.slider("Length", 0.001, 10000.0, 13.1, format="%.3f")
    if st.button("🦒 Stretch! 🌈"):
        factors = {
            'Meters':1,'Kilometers':1000,'Miles':1609.34,'Feet':0.3048,
            'Inches':0.0254, 'Centimeters':0.01
        }
        base = n_ln * factors[f_ln]
        out = base / factors[t_ln]
        st.markdown(f"<div class='bubble'>{n_ln:.3f} {f_ln} = {out:.3f} {t_ln} 🎈</div>", unsafe_allow_html=True)

# --- Weight ---
with tabs[3]:
    fun_anim("weight")
    st.subheader("Epic Weight Converter")
    ws = ['Kilograms','Grams','Pounds','Ounces']
    fr_w = st.selectbox("From", ws)
    to_w = st.selectbox("To", ws, index=2)
    wt = st.slider("Weight", 0.01, 2000.0, 70.0, step=0.01)
    if st.button("🏋️‍♂️ Lift! 💥"):
        wf = {'Kilograms':1,'Grams':0.001,'Pounds':0.453592,'Ounces':0.0283495}
        base = wt * wf[fr_w]
        out = base / wf[to_w]
        st.markdown(f"<div class='bubble'>{wt:.2f} {fr_w} = {out:.2f} {to_w} 🏆</div>", unsafe_allow_html=True)

# --- Playful footer ---
st.markdown("<center><b>✨ Every conversion’s a party! ✨<br>Streamlit Playground Edition</b></center>", unsafe_allow_html=True)
