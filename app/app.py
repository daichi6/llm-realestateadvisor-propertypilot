import streamlit as st
import time
from settings import setup, configure_display_options
from chatbot import chat_all

# Page configuration
st.set_page_config(page_title="PropertyPilot")

# Initialize storage for user accounts and chat histories in session state
if "users" not in st.session_state:
    st.session_state.users = {"user1": "password1", "user2": "password2"}
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}  # To store chat histories per user

# Function for the Sign-Up page
def signup_page():
    st.title("Sign Up for PropertyPilot")
    st.write("Create an account to get started.")

    new_username = st.text_input("Create a Username")
    new_password = st.text_input("Create a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up"):
        if new_username in st.session_state.users:
            st.error("Username already exists. Please choose a different one.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username and new_password:
            # Save the new user credentials in session state
            st.session_state.users[new_username] = new_password
            st.success("Sign-up successful! Please log in.")
            st.session_state.signup_success = True
            st.session_state.show_signup = False
            time.sleep(1)
            st.experimental_rerun()  # Refresh to go to the login page
        else:
            st.error("Please fill out all fields.")

# Function for the login page
def login_page():
    st.title("Login to PropertyPilot")
    st.write("Please log in to continue to the chat.")
    
    if st.session_state.get("signup_success"):
        st.success("Account created! Please log in.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username  # Track the logged-in user
            st.success("Login successful! Redirecting...")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
    
    st.write("Don't have an account?")
    if st.button("Go to Sign Up"):
        st.session_state.signup_success = False
        st.session_state.show_signup = True
        st.experimental_rerun()

# Function for the main chat app
def chat_app():
    st.title("PropertyPilot: InternationAlly")
    st.write("PropertyPilot is an AI-powered real estate assistant designed to assist you in your property search journey. Ask anything related to properties, neighborhoods, or real estate trends.")
    
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.current_user = None  # Clear the current user
        st.experimental_rerun()
    
    # Clear Conversation button to reset the chat history
    if st.button("Clear Conversation"):
        current_user = st.session_state.current_user
        st.session_state.chat_histories[current_user] = [{"role": "assistant", "content": "Hello! How can I assist you with your property search today?"}]
        st.success("Chat history cleared.")
        st.experimental_rerun()

    # Setup the bot and environment, but only once
    if 'setup_done' not in st.session_state:
        chat, prompts_dict, neighborhoods_info, neighborhoods_boundaries, vectordb = setup()
        configure_display_options()
        st.session_state.chat = chat
        st.session_state.prompts_dict = prompts_dict
        st.session_state.neighborhoods_info = neighborhoods_info
        st.session_state.neighborhoods_boundaries = neighborhoods_boundaries
        st.session_state.vectordb = vectordb
        st.session_state.setup_done = True

    # Load or initialize chat history for the current user
    current_user = st.session_state.current_user
    if current_user not in st.session_state.chat_histories:
        st.session_state.chat_histories[current_user] = [{"role": "assistant", "content": "Hello! How can I assist you with your property search today?"}]
    
    # Display chat messages from history
    for message in st.session_state.chat_histories[current_user]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for user to type messages
    if user_input := st.chat_input("Enter your query here:"):
        # Display user message
        st.session_state.chat_histories[current_user].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Retrieve the chatbot and related objects from session state
        chat = st.session_state.chat
        prompts_dict = st.session_state.prompts_dict
        neighborhoods_info = st.session_state.neighborhoods_info
        neighborhoods_boundaries = st.session_state.neighborhoods_boundaries
        vectordb = st.session_state.vectordb

        # Get chatbot response
        response, intent = chat_all(chat, prompts_dict, user_input, neighborhoods_info, neighborhoods_boundaries, vectordb)

        # Simulate gradual response with a spinner
        with st.chat_message("assistant"):
            placeholder = st.empty()  # Create a placeholder for the gradual text output
            gradual_text = ""

            with st.spinner("Thinking..."):
                for word in response.split():
                    gradual_text += word + " "
                    placeholder.markdown(gradual_text)  # Update the placeholder with the new word
                    time.sleep(0.05)

        # Add assistant response to the conversation history for the current user
        st.session_state.chat_histories[current_user].append({"role": "assistant", "content": response})

# Main app logic to control flow between login, sign-up, and chat pages
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

if not st.session_state.logged_in:
    if st.session_state.show_signup:
        signup_page()
    else:
        login_page()
else:
    chat_app()
