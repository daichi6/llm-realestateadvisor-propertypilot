import streamlit as st
import time
from frontend.app_elements import show_signup, load_image_as_base64

# Function for the login page
def login_page():
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
        <p style="font-size: 18px;">Sign in to get started.</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    
    # Login form container

    with st.form(key="login_form"):
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Username</p>", unsafe_allow_html=True)
        username = st.text_input("Username", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Password</p>", unsafe_allow_html=True)
        password = st.text_input("Password", type="password", label_visibility="collapsed")
        submit_button = st.form_submit_button("Sign In")
    
    if submit_button:
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username  # Track the logged-in user
            # Show success message
            st.markdown("<div class='st-success-box'>Sign-in successful ✅ Launching Ally 🤗</div>", unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
        else:
            st.markdown("<div class='st-error-box'>❌ Invalid username or password.</div>", unsafe_allow_html=True)

    # Sign-up prompt and button for new users
    st.markdown("<div class='signup-link'>New international student?</div>", unsafe_allow_html=True)


    # Apply the custom width by wrapping the button in a container
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])  # To center the button
        with col2:  # Place the button in the middle column
            if st.button("Sign Up Here", key="small-signup-button"):
                show_signup()
                st.rerun()