import streamlit as st

# Set the page title
st.title("🐦 Eagle's Greeting Form")
st.header("Day 1: Python Challenge")

# Create a form
with st.form("greeting_form"):
    # Name input
    name = st.text_input(
        "Enter your name:", 
        placeholder="Type your name here..."
    )

    # Age slider
    age = st.slider(
        "Select your age:", 
        min_value=1, 
        max_value=100, 
        value=25,
        help="Use the slider to select your age"
    )

    # Submit button
    submitted = st.form_submit_button("Generate Greeting 🎉")

# Display greeting when form is submitted
if submitted:
    if name.strip():  # Check if name is not empty
        st.success(f"🎊 Hello {name}! Welcome to the Python Challenge!")
        st.info(f"🎂 You are {age} years old - that's awesome!")

        # Add some fun based on age
        if age < 18:
            st.balloons()
            st.write("🌟 Young and energetic! Keep coding!")
        elif age < 30:
            st.write("🚀 Perfect age for learning new technologies!")
        elif age < 50:
            st.write("🧠 Experience meets innovation!")
        else:
            st.write("🏆 Wisdom and coding - what a great combination!")
    else:
        st.error("Please enter your name to get a greeting!")

# Add some styling and footer
st.markdown("---")
st.markdown("### 🔥 15 Days Python Challenge")
st.markdown("*Built with Streamlit* ❤️")