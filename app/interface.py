from settings import setup, configure_display_options
from chatbot import chat_all

# Setup
chat, prompts_dict, neighborhoods_info, neighborhoods_boundaries, vectordb = setup()
configure_display_options()

# Chatbot loop
while True:
    user_query = input("Please enter your query (type 'exit' to quit): ")
    
    if user_query.lower() == 'Exit':
        print("Exiting the chatbot. Goodbye!")
        break
    
    # Call the chat_all function with the user's query
    chat_all(chat, prompts_dict, user_query, neighborhoods_info, neighborhoods_boundaries, vectordb)