import streamlit as st
import pandas as pd
from io import StringIO

# -------- UI configuration --------
st.set_page_config(
    page_title="Event Registration System",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------- Core data storage --------
if 'registrations' not in st.session_state:
    st.session_state['registrations'] = []

# -------- Sidebar (Organizer Tools) --------
with st.sidebar:
    st.header("Organizer Tools")
    st.write("Total registrations: **{}**".format(len(st.session_state['registrations'])))
    if len(st.session_state['registrations']) > 0:
        df = pd.DataFrame(st.session_state['registrations'])
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Export CSV",
            data=csv_buffer.getvalue(),
            file_name="event_registrations.csv",
            mime="text/csv"
        )
    else:
        st.info("No registrations yet to export.")

# -------- Registration Form --------
st.markdown(
    """
    <style>
    .main {background-color: #FAFAFA;}
    .stTextInput > label, .stEmailInput > label, .stSelectbox > label {
        font-size:1.1em;font-weight:500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎉 Event Registration")

st.write(
    "Fill out the form below to register for your chosen event. All information is kept confidential."
)

with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("Full Name", max_chars=100)
    email = st.text_input("Email", max_chars=100, help="We'll never share your email.")
    event = st.selectbox(
        "Event Choice",
        ["Select an event...", "Tech Talk", "Workshop", "Networking", "Product Demo"]
    )
    submitted = st.form_submit_button("Register")

    if submitted:
        # ---- Validation ----
        errors = []
        if not name.strip():
            errors.append("Name is required.")
        if not email.strip() or "@" not in email:
            errors.append("Valid email is required.")
        if event == "Select an event...":
            errors.append("Choose a valid event.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            registration = {"Name": name.strip(), "Email": email.strip(), "Event": event}
            st.session_state['registrations'].append(registration)
            st.success("Thank you for registering! Your response has been recorded.")

# -------- Live Registration Count --------
st.subheader("Current Registration Count")
st.markdown(
    f"""
    <div style="font-size:2em;font-weight:600;color:#337ab7;padding:10px 0;">
        {len(st.session_state['registrations'])} Registered
    </div>
    """,
    unsafe_allow_html=True
)

# -------- Registration Data View (for transparency) --------
if len(st.session_state['registrations']) > 0:
    st.subheader("Recent Registrations")
    df_recent = pd.DataFrame(st.session_state['registrations']).tail(5).reset_index(drop=True)
    st.dataframe(
        df_recent.style.format(na_rep="-"),
        use_container_width=True,
        hide_index=True,
        height=225
    )
else:
    st.info("No registrations yet. Be the first to sign up!")
