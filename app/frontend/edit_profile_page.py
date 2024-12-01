import streamlit as st
import time

# Function to edit the profile
def edit_profile_page():
    current_user = st.session_state.current_user
    first_name = st.session_state.users.get(current_user, {}).get("first_name", "")
    user_data = st.session_state.user_onboarding_data.get(current_user, {})

    st.markdown(f"<div style='text-align: center; font-size: 30px; font-weight: bold;'>Edit Your Profile, {first_name}!</div>", unsafe_allow_html=True)

    with st.form(key='edit_profile_form'):
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Your hometown or country</p>", unsafe_allow_html=True)
        place_of_origin = st.text_input("Your hometown or country:", value=user_data.get("place_of_origin", ""), key="edit_place_of_origin", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Your destination city in the US</p>", unsafe_allow_html=True)
        us_city = st.text_input("Your destination city in the US:", value=user_data.get("us_city", ""), key="edit_us_city", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Your school/college</p>", unsafe_allow_html=True)
        us_college = st.text_input("Your school/college:", value=user_data.get("us_college", ""), key="edit_us_college", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Do you have a student health insurance? (Yes/No)</p>", unsafe_allow_html=True)
        us_insurance = st.text_input("Do you have a student health insurance?", value=user_data.get("us_insurance", ""), key="edit_us_insurance", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Do you have a Social Security Number? (Yes/No)</p>", unsafe_allow_html=True)
        us_ssn = st.text_input("Do you have a Social Security Number?", value=user_data.get("us_ssn", ""), key="edit_us_ssn", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Did you find a place to stay in the US? (Yes/No)</p>", unsafe_allow_html=True)
        us_place_to_stay = st.text_input("Did you find a place to stay in the US?", value=user_data.get("us_place_to_stay", ""), key="edit_us_place_to_stay", label_visibility="collapsed")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#333333;'>Something about you</p>", unsafe_allow_html=True)
        us_other = st.text_input("About you:", value=user_data.get("us_other", ""), key="edit_us_other", label_visibility="collapsed")

        save_button = st.form_submit_button("Save Changes")

    if save_button:
        # Save the updated data to the session state
        st.session_state.user_onboarding_data[current_user] = {
            "place_of_origin": place_of_origin.strip(),
            "us_city": us_city.strip(),
            "us_college": us_college.strip(),
            "us_insurance": us_insurance.strip(),
            "us_ssn": us_ssn.strip(),
            "us_place_to_stay": us_place_to_stay.strip(),
            "us_other": us_other.strip(),
        }

        st.session_state.editing_profile = False  # Exit profile editing mode
        # st.success("Profile updated successfully!")
        st.markdown("<div class='st-success-box'>✅ Profile updated successfully!</div>", unsafe_allow_html=True)
        time.sleep(1)  # Add slight delay for better UX
        st.rerun()  # Redirect to chat screen