import streamlit as st
from frontend.app_elements import load_image_as_base64

def onboarding_page():
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

    current_user = st.session_state.current_user
    first_name = st.session_state.users[current_user]["first_name"]

    # Step 1: Ask about the user's origin
    if st.session_state.onboarding_step == 1:
        st.markdown(f"<div style='text-align: center; font-size: 30px;'>Hey {first_name}, let's get to know you better!</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 20px; margin-top: 20px; margin-bottom: 5px;'>Where are you from, {first_name}?</div>", unsafe_allow_html=True)
        
        # Input for place of origin
        place_of_origin = st.text_input("Your hometown or country:", key="place_of_origin", label_visibility="collapsed", placeholder="Enter your hometown or country")
        
        # Next button to proceed to the second step
        if st.button("Next"):
            if place_of_origin.strip():  # Ensure the user entered something
                # Save the response
                st.session_state.user_onboarding_data[current_user] = {
                    "place_of_origin": place_of_origin.strip()
                }
                st.session_state.onboarding_step = 2  # Move to the next step
                st.rerun()
            else:
                st.markdown("<div class='st-error-box'>❗ Please tell us where you're from to proceed.</div>", unsafe_allow_html=True)

    # Step 2: Ask about the city the user is moving to
    elif st.session_state.onboarding_step == 2:
        st.markdown(f"<div style='text-align: center; font-size: 30px;'>Hey {first_name}, let's get to know you better!</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 20px; margin-top: 20px; margin-bottom: 5px;'>Which city are you moving to in the US?</div>", unsafe_allow_html=True)
        
        # Input for city in the US
        us_city = st.text_input("Your destination city in the US:", key="us_city", label_visibility="collapsed", placeholder="Enter the city name")

        # Finish Sign Up button
        if st.button("Next"):
            if us_city.strip():  # Ensure the user entered something
                # Save the response
                st.session_state.user_onboarding_data[current_user]["us_city"] = us_city.strip()
                st.session_state.onboarding_step = 3  # Move to the next step
                st.rerun()
            else:
                st.markdown("<div class='st-error-box'>❗ Please tell us your destination city to complete the onboarding.</div>", unsafe_allow_html=True)

    # Step 3: Ask about the college the user is attending
    elif st.session_state.onboarding_step == 3:
        st.markdown(f"<div style='text-align: center; font-size: 30px;'>Hey {first_name}, let's get to know you better!</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 20px; margin-top: 20px; margin-bottom: 5px;'>Which school are you attending in the US?</div>", unsafe_allow_html=True)
        
        # Input for city in the US
        us_college = st.text_input("Your school/college:", key="us_college", label_visibility="collapsed", placeholder="Enter the school/college name")

        # Finish Sign Up button
        if st.button("Next"):
            if us_college.strip():  # Ensure the user entered something
                # Save the response
                st.session_state.user_onboarding_data[current_user]["us_college"] = us_college.strip()
                st.session_state.onboarding_step = 4  # Move to the next step
                st.rerun()
            else:
                st.markdown("<div class='st-error-box'>❗ Please tell us your school/college to complete the onboarding.</div>", unsafe_allow_html=True)

    # Step 4
    elif st.session_state.onboarding_step == 4:
        st.markdown(f"<div style='text-align: center; font-size: 30px;'>Hey {first_name}, let's get to know you better!</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 20px; margin-top: 20px; margin-bottom: 5px;'>Do you have a student health insurance?</div>", unsafe_allow_html=True)
        
        # Input for city in the US
        us_insurance = st.text_input("Do you have a student health insurance?:", key="us_insurance", label_visibility="collapsed", placeholder="Do you have a student health insurance? (Yes/No)")

        # Finish Sign Up button
        if st.button("Next"):
            if us_insurance.strip():  # Ensure the user entered something
                # Save the response
                st.session_state.user_onboarding_data[current_user]["us_insurance"] = us_insurance.strip()
                st.session_state.onboarding_step = 5  # Move to the next step
                st.rerun()
            else:
                st.markdown("<div class='st-error-box'>❗ Please tell us your whether you have a student health insurance so that Ally could better serve you.</div>", unsafe_allow_html=True)

    # Step 5
    elif st.session_state.onboarding_step == 5:
        st.markdown(f"<div style='text-align: center; font-size: 30px;'>Hey {first_name}, let's get to know you better!</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 20px; margin-top: 20px; margin-bottom: 5px;'>Do you have a Social Security Number?</div>", unsafe_allow_html=True)
        
        # Input for city in the US
        us_ssn = st.text_input("Do you have a Social Security Number?:", key="us_ssn", label_visibility="collapsed", placeholder="Do you have a Social Security Number? (Yes/No)")

        # Finish Sign Up button
        if st.button("Next"):
            if us_ssn.strip():  # Ensure the user entered something
                # Save the response
                st.session_state.user_onboarding_data[current_user]["us_ssn"] = us_ssn.strip()
                st.session_state.onboarding_step = 6  # Move to the next step
                st.rerun()
            else:
                st.markdown("<div class='st-error-box'>❗ Please tell us your whether you have a Social Security Number so that Ally could better serve you.</div>", unsafe_allow_html=True)

    # Step 6
    elif st.session_state.onboarding_step == 6:
        st.markdown(f"<div style='text-align: center; font-size: 30px;'>Hey {first_name}, let's get to know you better!</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 20px; margin-top: 20px; margin-bottom: 5px;'>Did you find a place to stay in the US?</div>", unsafe_allow_html=True)
        
        # Input for city in the US
        us_place_to_stay = st.text_input("Did you find a place to stay in the US?", key="us_place_to_stay", label_visibility="collapsed", placeholder="Did you find a place to stay in the US?")

        # Finish Sign Up button
        if st.button("Next"):
            if us_place_to_stay.strip():  # Ensure the user entered something
                # Save the response
                st.session_state.user_onboarding_data[current_user]["us_place_to_stay"] = us_place_to_stay.strip()
                st.session_state.onboarding_step = 7  # Move to the next step
                st.rerun()
            else:
                st.markdown("<div class='st-error-box'>❗ Ally could help you with searching for rental properties if you let us know.</div>", unsafe_allow_html=True)


    # Step 7
    elif st.session_state.onboarding_step == 7:
        st.markdown(f"<div style='text-align: center; font-size: 30px;'>Almost there, {first_name}!</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 20px; margin-top: 20px; margin-bottom: 5px;'>Write anything about yourself which you think would be useful for Ally to help you better.</div>", unsafe_allow_html=True)
        
        # Input for city in the US
        us_other = st.text_input("Write about yourself:", key="us_other", label_visibility="collapsed", placeholder="About you")

        # Finish Sign Up button
        if st.button("Finish Sign Up"):
            if us_other.strip():  # Ensure the user entered something
                # Save the response
                st.session_state.user_onboarding_data[current_user]["us_other"] = us_other.strip()
                # Redirect to login page
                st.session_state.show_onboarding = False
                st.session_state.show_signup = False
                st.session_state.onboarding_step = 1  # Move to the next step
                st.rerun()
            else:
                st.markdown("<div class='st-error-box'>❗ Although it's totally optional, please tell us about yourself. 🤗</div>", unsafe_allow_html=True)
