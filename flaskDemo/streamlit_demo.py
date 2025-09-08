import streamlit as st
from datetime import datetime

# --- SESSION STATE ---
if "posts" not in st.session_state:
    st.session_state["posts"] = []  # Each post = {user, text, time, likes}

st.title("📱 Mini Social Network")

# --- Create Post ---
st.subheader("Create a Post")
user = st.text_input("Your name")
post_text = st.text_area("What's on your mind?")
if st.button("Post"):
    if user.strip() and post_text.strip():
        st.session_state["posts"].insert(
            0,
            {"user": user, "text": post_text, "time": datetime.now(), "likes": 0},
        )
        st.success("✅ Posted successfully!")
    else:
        st.warning("Please enter your name and a post.")

# --- News Feed ---
st.subheader("News Feed")
if st.session_state["posts"]:
    for i, post in enumerate(st.session_state["posts"]):
        st.markdown(f"**{post['user']}** 🕒 {post['time'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(post["text"])
        if st.button(f"👍 {post['likes']} Likes", key=f"like_{i}"):
            st.session_state["posts"][i]["likes"] += 1
        st.divider()
else:
    st.info("No posts yet. Be the first to share something!")
