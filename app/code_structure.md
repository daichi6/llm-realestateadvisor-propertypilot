# Code Structure

This document provides an overview of the project's file structure and their purposes.


### Main Files

- [`app.py`](./app.py): The main Streamlit script that serves as the entry point for the application.
- [`llm.py`](./llm.py): Defines the basic configurations for the LLM (Gemini).
- [`chatbot.py`](./chatbot.py): Contains functions that utilize the LLM for generating responses.
- [`property_info.py`](./property_info.py): Includes functions for property searches using the Zillow API.
- [`local_advisor.py`](./local_advisor.py): Holds functions related to the Local Advisor feature, which leverages the Google API.
- [`vector_search.py`](./vector_search.py): Provides functions for vector search and Retrieval-Augmented Generation (RAG), designed to support international students.
- [`vectordb_creation.py`](./vectordb_creation.py): Includes functions for creating and managing vector databases, aimed at international student support.
- [`map_creation.py`](./map_creation.py): Contains functions for generating maps, integrating with location data.
- [`prompt_creation.py`](./prompt_creation.py): Contains functions for generating prompts used across different parts of the application.
- [`settings.py`](./settings.py): Manages configurations such as loading prompts and vector databases, as well as other settings.

---

### Frontend

Files located in the `app/frontend/` folder:
- [`app_elements.py`](./frontend/app_elements.py): Contains reusable utility functions for the frontend application, such as page toggle and image loading.
- [`chatapp.py`](./frontend/chatapp.py): Defines and manages the main Streamlit chat interface, including chat box functionality and user interactions.
- [`edit_profile_page.py`](./frontend/edit_profile_page.py): Implements the Streamlit page for editing user profile information within the chat interface.
- [`login_page.py`](./frontend/login_page.py): Manages the Streamlit login page, handling user authentication and input validation.
- [`onboarding_page.py`](./frontend/onboarding_page.py): Creates the Streamlit onboarding flow, including loading introductory questions and saving user responses for personalization.
- [`signup_page.py`](./frontend/signup_page.py): Handles the Streamlit sign-up process, facilitating new user registration and data submission.

---

### Prompts Folder

Files located in the `app/prompts/` folder:
- Contains prompt files saved in `.txt` format, which are used throughout the application.
