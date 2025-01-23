import streamlit as st
import pandas as pd
import os
from streamlit_star_rating import st_star_rating  # Import the star rating widget

# Define the storage path
storage_path = r"C:\Users\CHS8SH\Streamlit\Feedback"
if not os.path.exists(storage_path):
    os.makedirs(storage_path)

def save_feedback(name, rating, feedback):
    csv_path = os.path.join(storage_path, "feedback.csv")
    new_entry = pd.DataFrame({"Name": [name], "Rating": [rating], "Feedback": [feedback]})

    if os.path.exists(csv_path):
        existing_data = pd.read_csv(csv_path)
        combined_data = pd.concat([existing_data, new_entry], ignore_index=True)
    else:
        combined_data = new_entry

    combined_data.to_csv(csv_path, index=False)

# Streamlit App
st.title("Experience World Feedback Form")

with st.form("feedback_form"):
    name = st.text_input("Name", placeholder="Your name..", max_chars=50)

    # Use the st_star_rating widget
    st.write("Please rate your overall experience with us:")
    rating = st_star_rating(
        label=None,              # Optional label
        maxValue=5,              # Number of stars
        defaultValue=0,          # Default selected stars
        size=30,                 # Size of the stars
        emoticons=False,         # Use stars instead of emoticons
        dark_theme=False,        # Light theme
    )

    feedback = st.text_area("Feedback", placeholder="Write something...")
    
    # Submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
        if name.strip() and feedback.strip():
            save_feedback(name, rating, feedback)
            st.success(f"Thank you for your feedback! You rated the app {rating} star{'s' if rating > 1 else ''}.")
        else:
            st.error("Please fill out all fields before submitting.")

st.markdown("---")
st.header("Download Feedback Data")

csv_path = os.path.join(storage_path, "feedback.csv")
if os.path.exists(csv_path):
    with open(csv_path, "rb") as file:
        st.download_button("Download Feedback CSV", file, file_name="feedback.csv", mime="text/csv")
else:
    st.info("No feedback data available yet.")
