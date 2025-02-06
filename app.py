import streamlit as st
import time
from streamlit_star_rating import st_star_rating
from pymongo import MongoClient

# Corrected MongoDB URI (disabled retryable writes)
MONGO_URI = "mongodb://experience_world:EW%402025@10.58.114.165:27017/admin?ssl=false&directConnection=true&retryWrites=false"
client = MongoClient(MONGO_URI)

# Use the existing "local" database and "EW_feedbacks" collection
db = client["local"]
collection = db["EW_feedbacks"]

# Function to save feedback to MongoDB
def save_feedback_to_mongodb(name, rating, feedback):
    feedback_data = {"name": name, "rating": rating, "feedback": feedback}
    collection.insert_one(feedback_data)  # Insert into MongoDB

st.image("Logo.png", use_container_width=True)

# Streamlit App
st.title("Experience World Feedback Form")

with st.form("feedback_form"):
    name = st.text_input("Name", placeholder="Your name..", max_chars=50)

    # Star Rating Widget
    st.write("Please rate your overall experience with us:")
    rating = st_star_rating(
        label=None,
        maxValue=5,
        defaultValue=0,
        size=30,
        emoticons=False,
        dark_theme=False,
    )

    feedback = st.text_area("Feedback", placeholder="Write something...")

    # Submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
        if name.strip() and feedback.strip():
            save_feedback_to_mongodb(name, rating, feedback)
            st.success(f"Thank you for your feedback! You rated us {rating} star{'s' if rating > 1 else ''}.")
            time.sleep(3)  # Wait for 3 seconds
            st.markdown(
                """
                <meta http-equiv="refresh" content="0">
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error("Please fill out all fields before submitting.")

st.markdown(
    """
    <div style="margin-top: 20px; padding: 15px; border: 2px solid #e8e8e8; background-color: #ffffff; border-radius: 8px;">
        <strong style="font-size: 16px;">⚠️ Please do not enter any personal or sensitive data.</strong><br>
        Alternatively, you can send us an email at experience.world@bcn.bosch.com
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
