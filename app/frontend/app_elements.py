import streamlit as st
import base64

# Toggle the sign-up page
def show_signup():
    st.session_state.show_signup = True

# Toggle the login page
def show_login():
    st.session_state.show_signup = False

# Function to load and convert an image file to base64 string
def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
def preprocess_markdown(text):
    # Fix inconsistent bold and italic syntax
    text = text.replace("* **", "\n\n**").replace(" * ", "\n\n- **").replace("* **Link:**", "- **Link:**")

    # Ensure links are properly formatted
    text = text.replace("(https://", "[View on Zillow](https://")

    # Fix broken list formatting
    text = text.replace("\n*", "\n- ")

    # Add double line breaks between sections for readability
    text = text.replace("\n\n-", "\n\n- ")

    return text