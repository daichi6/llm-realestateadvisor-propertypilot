import streamlit as st
import re
from frontend.app_elements import show_login, load_image_as_base64

# Function for the Sign-Up page
def signup_page():
    # Load and convert the logo image
    logo_base64 = load_image_as_base64("ally-logo.png")  # Ensure the path is correct

    # Display the centered logo using HTML and Base64
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;">
            <img src="data:image/jpg;base64,{logo_base64}" width="80">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='main-title'>InternationAlly by PropertyPilot</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="display: flex; justify-content: center; text-align: center; margin-top: 1px;">
            <p style="font-size: 30px;">Your Ally Abroad! 🚀</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="display: flex; justify-content: center; text-align: center; margin-top: 20px;">
            <p style="font-size: 18px;">Create an account to access Ally, your trusted international student advisor.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form(key='signup_form'):

        # New fields for user details
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>First Name</p>", unsafe_allow_html=True)
        first_name = st.text_input("First Name", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Last Name</p>", unsafe_allow_html=True)
        last_name = st.text_input("Last Name", label_visibility="collapsed")

        # New field for email
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Email</p>", unsafe_allow_html=True)
        email = st.text_input("Email", label_visibility="collapsed")

        # Existing fields for username and password
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Create a Username</p>", unsafe_allow_html=True)
        new_username = st.text_input("Create a Username", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Create a Password</p>", unsafe_allow_html=True)
        new_password = st.text_input("Create a Password", type="password", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Confirm Password</p>", unsafe_allow_html=True)
        confirm_password = st.text_input("Confirm Password", type="password", label_visibility="collapsed")

        submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        # Sanity check for email format using regex
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        # Check if all fields are filled
        if not first_name or not last_name:
            st.markdown("<div class='st-error-box'>❗ Please fill out all personal details.</div>", unsafe_allow_html=True)
        elif not email:
            st.markdown("<div class='st-error-box'>❗ Please provide an email address.</div>", unsafe_allow_html=True)
        elif not re.match(email_pattern, email):
            st.markdown("<div class='st-error-box'>❗ Invalid email format. Please enter a valid email address.</div>", unsafe_allow_html=True)
        elif new_username in st.session_state.users:
            st.markdown("<div class='st-error-box'>❗ Username already exists. Please choose a different one.</div>", unsafe_allow_html=True)
        elif new_password != confirm_password:
            st.markdown("<div class='st-error-box'>❗ Passwords do not match.</div>", unsafe_allow_html=True)
        elif new_username and new_password and re.match(email_pattern, email):
            # Save the new user credentials and details in session state
            st.session_state.users[new_username] = {
                "password": new_password,
                "first_name": first_name,
                "last_name": last_name,
                "email": email  # Save email along with other details
            }
            st.session_state.current_user = new_username
            st.session_state.onboarding_step = 1  # Reset to the first onboarding step
            st.session_state.show_onboarding = True  # Trigger onboarding page
            st.rerun()  # Redirect to the onboarding page

        else:
            st.markdown("<div class='st-error-box'>❗ Please fill out all fields.</div>", unsafe_allow_html=True)

    # Add "Already have an account?" text and "Sign In" button below the sign-up form
    st.markdown("<div class='signup-link'>Already have an account?</div>", unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])  # To center the button
        with col2:  # Place the button in the middle column
            if st.button("Back to Sign In", key="small-backtosignin-button"):
                show_login()
                st.rerun()


