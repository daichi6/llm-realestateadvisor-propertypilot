import streamlit as st
import os
from dotenv import load_dotenv
from map_creation import get_default_chicago_map_config, render_map
from frontend.onboarding_page import onboarding_page
from frontend.signup_page import signup_page
from frontend.login_page import login_page
from frontend.chatapp import chat_app

# Load the API key for Google Maps from .env
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("DEV_GOOGLE_MAP_API_KEY")

# Page configuration
st.set_page_config(page_title="InternationAlly", page_icon="ally-logo.png", layout="centered")

# Custom CSS for styling font, colors, and form layout
st.markdown("""
    <style>

        [data-testid=stSidebar] {
        background-color: #ffffff;
        }

        /* Change the font family and colors for the main app */
        html, body, [class*="css"]  {
            font-family: 'Open Sans', sans-serif !important;
            color: #333333;  /* Main text color */

        }

        /* Center title styling */
        .main-title {
            color: #434343;
            font-family: 'Open Sans', sans-serif !important;
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }

        /* Form styling */
        .form-container {
            margin-top: 100px;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }

        button {
            height: auto;
            padding-top: 15px !important;
            padding-bottom: 15px !important;
            margin-bottom: -5px !important;
        }

        /* Customize button colors */
        .stButton>button {
            color: #FFFFFF !important; 
            background-color: #9AD6D2 !important;
            border: none;
            margin-top: 10px;
            padding: 8px 16px;
            font-weight: bold;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #86cec9 !important;  /* Darker on hover */
            color: #FFFFFF !important;
        }
        .stButton>button:active {
            background-color: #86cec9 !important; /* Keep the same background color when clicked */
            color: #FFFFFF !important;  /* Keep the text color white when clicked */
        }
         
        /* Input field styling */
        .stTextInput, .stPasswordInput {
            background-color: #ffffff;
            border-radius: 4px;
            padding: 0px;
            width: 100%;
            margin-top: 0px;
        }

        /* Link styling */
        .signup-link {
            text-align: center;
            margin-top: 20px;
            font-weight: bold;
            font-size: 20px;
        }
            
        /* Success message box */
        .st-success-box {
            color: #55555C;
            background-color: #FFF8E8;
            padding: 10px;
            border-radius: 1px;
            font-weight: bold;
            margin: 10px 0;
        }

        /* Error message box */
        .st-error-box {
            color: #55555C;
            background-color: #F4E5E3;
            padding: 10px;
            border-radius: 1px;
            font-weight: bold;
            margin: 10px 0;
        }
            
        /* Adjust the height of input fields */
        input[type="text"], input[type="password"] {
            height: 55px;              /* Sets a fixed height */
            font-size: 18px;           /* Increases the font size */
            width: 100%;               /* Makes input full-width of its container */
            padding: 12px;             /* Adds space inside the input for a larger clickable area */
            color: #333333;            /* Sets text color */
            /* background-color: #f9f9f9; Sets background color of input */
            border-radius: 1px;        /* Rounds the corners */
            outline: none;             /* Removes the default outline when input is focused */
            box-shadow: none;          /* Removes default box shadow */
            transition: all 0.3s ease; /* Adds a smooth transition for hover or focus effects */
        }
            
        .css-1d391kg {  /* This class targets the sidebar in Streamlit */
            top: 0;
            left: 0;
            height: 100vh;
            background-color: #ffffff;
            padding-top: 1rem;
            z-index: 100;
            width: 100px;  /* Set the desired sidebar width here */
        }
        
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if "users" not in st.session_state:
    st.session_state.users = {"user1": {"password": "password1"}, "user2": {"password": "password2"}}
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}  # To store chat histories per user
if "current_map_html" not in st.session_state:
    # Set the initial map to be centered on Chicago
    default_map_config = get_default_chicago_map_config()
    st.session_state.current_map_html = render_map(GOOGLE_MAPS_API_KEY, **default_map_config)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "show_onboarding" not in st.session_state:
    st.session_state.show_onboarding = False
if "user_onboarding_data" not in st.session_state:
    st.session_state.user_onboarding_data = {}
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 1  # Start at step 1


## Run App ##

if not st.session_state.logged_in:
    if st.session_state.show_onboarding:
        onboarding_page()
    elif st.session_state.show_signup:
        signup_page()
    else:
        login_page()
else:
    chat_app()

