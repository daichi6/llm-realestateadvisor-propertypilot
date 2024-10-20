from settings import setup, configure_display_options
from chatbot import chat_all

# setup
chat, prompts_dict, neighborhoods_info, neighborhoods_boundaries, vector_store = setup()
configure_display_options()

# chatbot
# user_query = "Hello, how are you?" 
user_query = "I'm looking for an apartment in Gold Coast with 1 bedroom, montly rent between $2000 and $3500. Give me links if you have them." 
# user_query = "What are the top rated Japanese restaurants on the north side of chicago? Give me Yelp links if you have them."
# user_query = "What is the Hyde Park in Chicago like?"
chat_all(chat, prompts_dict, user_query, neighborhoods_info, neighborhoods_boundaries, vector_store)