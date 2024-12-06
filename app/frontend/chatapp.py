import streamlit as st
import time
from settings import setup, configure_display_options
from chatbot import chat_all
from frontend.app_elements import load_image_as_base64, preprocess_markdown
from frontend.edit_profile_page import edit_profile_page

def chat_app():
    # Setup the bot and environment, but only once
    if 'setup_done' not in st.session_state:
        chat, prompts_dict, vectordb = setup()
        configure_display_options()
        st.session_state.chat = chat
        st.session_state.prompts_dict = prompts_dict
        st.session_state.vectordb = vectordb
        st.session_state.setup_done = True
        st.session_state.current_map_html = None  # Initialize with no map displayed

    # Ensure the current user and chat history are initialized
    current_user = st.session_state.current_user

    # Fetch the user's first name if available, default to "there"
    first_name = st.session_state.users.get(current_user, {}).get("first_name", "there")

    if current_user not in st.session_state.chat_histories:

        print(current_user)

        if (current_user == "user1") or (current_user == 'user2'):
            print("Entered.")
            st.session_state.user_onboarding_data[current_user] = {
                    "place_of_origin": 'Tokyo, Japan',
                    "us_city": 'Chicago, IL',
                    "us_college": 'The University of Chicago',
                    "us_insurance": "No",
                    "us_ssn": 'No',
                    "us_place_to_stay": "No",
                    "us_other": "I love Japanese food.",
                    "first_name": "John"
                }
        
        if (current_user != "user1") and (current_user != 'user2'):
            st.session_state.user_onboarding_data[current_user]["first_name"] = first_name

        print(st.session_state.user_onboarding_data)

        from llm import start_chat_session, get_chat_response

        # Start a new chat session
        welcome_chat = start_chat_session()

        # Test the chat session with a simple prompt
        welcome_prompt = f'''Hi! You are an empathetic, polite, helpful international student advisor who helps international students with a range of services like finding them a place to stay (property search), local advising on neighborhoods and places of interest (restaurants, grocery stores, attractions, public transportation, fitness centers, etc.), and also about student essentials like health insurance, visa, etc..
        
        Based on the information the user has given so far, I want you to generate a question template like below:

        Template: Hello {first_name}! I know being an international student can feel like a lot, especially in a place like the U.S., where everything might feel new and different. How are you feeling about everything so far? Any specific areas where you’re feeling like you could use a bit of help or extra advice?

        This template should change based on the demands of the user defined through the user profile. 

        Here's the current user profile:
        User hometown: {st.session_state.user_onboarding_data[current_user]['place_of_origin']}
        User destination: {st.session_state.user_onboarding_data[current_user]['us_city']}
        User school: {st.session_state.user_onboarding_data[current_user]['us_college']}
        User have health insurance?: {st.session_state.user_onboarding_data[current_user]['us_insurance']}
        User have SSN?: {st.session_state.user_onboarding_data[current_user]['us_ssn']}
        User found a place to stay in the US?: {st.session_state.user_onboarding_data[current_user]['us_place_to_stay']}
        User other information: {st.session_state.user_onboarding_data[current_user]['us_other']}

        If the user haven't given a lot of info, you are free to make your own assumptions.

        Give one good question template as the response to me which shows an international student advisor concern towards their students.
        '''
        welcome_response = get_chat_response(welcome_chat, welcome_prompt)
        print("Response:", welcome_response)

        st.session_state.chat_histories[current_user] = [
            {
                "role": "assistant",
                "content": welcome_response,
            }
        ]
    
    # Check if the user is editing their profile
    if st.session_state.get("editing_profile", False):
        edit_profile_page()
        return

    # Sidebar content with logo, description, and buttons
    # Sidebar content with logo, description, and buttons at the bottom
    with st.sidebar:
        st.markdown(
            """
            <style>
                .sidebar-buttons {
                    position: absolute;
                    bottom: 100px; /* Adjust distance from the bottom */
                    width: calc(100% - 2rem); /* Ensure buttons take full width minus padding */
                    padding: 0 1rem;
                }
                .sidebar-content {
                    margin-bottom: 50px; /* Space to account for bottom buttons */
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Sidebar content above the buttons
        st.markdown(
            """
            <div class="sidebar-content">
                <div style="text-align: center;">
                    <img src="data:image/jpg;base64,{}" width="80">
                </div>
                <div style="text-align: center; font-size: 30px; font-weight: bold; margin-top: 10px; font-family: 'Open Sans', sans-serif;">
                    InternationAlly by PropertyPilot
                </div>
                <div style="text-align: center; font-size: 22px;">
                    Your Ally Abroad! 🚀
                </div>
            </div>
            """.format(load_image_as_base64("ally-logo.png")),  # Ensure the path is correct
            unsafe_allow_html=True
        )

        # Buttons positioned at the bottom
        with st.container():
            st.markdown('<div class="sidebar-buttons">', unsafe_allow_html=True)
            if st.button("Clear Conversation"):
                st.session_state.chat_histories[current_user] = [
                    {
                        "role": "assistant",
                        "content": f"Hello {first_name}! I know being an international student can feel like a lot, especially in a place like the U.S., where everything might feel new and different. How are you feeling about everything so far? Any specific areas where you’re feeling like you could use a bit of help or extra advice?"
                    }
                ]
                st.session_state.current_map_html = None  # Clear map when clearing chat
                st.success("Chat history cleared.")
                st.rerun()

            if st.button("Edit Profile"):
                st.session_state.editing_profile = True  # Toggle to profile editing mode
                st.rerun()

            if st.button("Log Out"):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)


    # Main chat UI

    # Display chat messages
    for message in st.session_state.chat_histories[current_user]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for user to type messages
    if user_input := st.chat_input("Enter your query here:"):
        st.session_state.chat_histories[current_user].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Process the user input with the chatbot
        response, map_html, intent = chat_all(
            st.session_state.chat,
            st.session_state.prompts_dict,
            user_input,
            st.session_state.vectordb,
            st.session_state.user_onboarding_data[current_user]
        )

        # Display the chatbot's response
        with st.chat_message("assistant"):
            placeholder = st.empty()
            gradual_text = ""

            with st.spinner("Thinking..."):
                for word in response.split():
                    gradual_text += word + " "
                    placeholder.text(gradual_text)
                    time.sleep(0.05)

            # Finalize the placeholder with the complete response - Will
            # response = preprocess_markdown(response)
            placeholder.markdown(response)

        # Add the response to chat history
        st.session_state.chat_histories[current_user].append({"role": "assistant", "content": response})

        # Update the map if needed
        if map_html and map_html != st.session_state.current_map_html:
            st.session_state.current_map_html = map_html
        else:
            st.session_state.current_map_html = None  # Set to None if no map is provided

    # Conditionally display the map only if there is content
    if st.session_state.get("current_map_html"):
        st.components.v1.html(st.session_state.current_map_html, height=500, width=710)  # Adjust height and width as needed