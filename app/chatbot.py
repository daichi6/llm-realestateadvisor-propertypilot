import os
from property_info import extract_json_to_dict, fetch_top_properties_detail
from map_creation import create_property_map, create_local_advisor_map
from local_advisor import generate_local_search_query, search_google_places, generate_local_advisor_response
from prompt_creation import (
    generate_prompt_classifier,
    generate_prompt_property,
    generate_prompt_apifilter,
    generate_prompt_rag_international,
    generate_prompt_general,
    generate_prompt_rewrite_query
)
from llm import get_chat_response
from vector_search import search_similar_chunks, format_chunk_results, reciprocal_rank_fusion
import json

GOOGLE_MAPS_API_KEY = os.getenv("PROD_GOOGLE_MAP_API_KEY")


# initial intent classifier
def intent_classifier(chat, prompts_dict, user_query):
    prompt = generate_prompt_classifier(prompts_dict['instruction_classifier'], user_query)
    response = get_chat_response(chat, prompt)
    print('Intent Number:', int(response))
    return int(response)


# get property through zollow api
def get_listings_from_zillow(chat, prompts_dict, user_query):
    prompt = generate_prompt_apifilter(prompts_dict['instruction_apifilter'], user_query, locations_string = prompts_dict['zillow_locations'])
    api_filter = get_chat_response(chat, prompt)
    api_filter = extract_json_to_dict(api_filter)
    top_properties = fetch_top_properties_detail(api_filter)
    return top_properties
    

# get final response for property search
def get_final_response_property(chat, prompts_dict, user_query, property_info, user_profile):
    prompt = generate_prompt_property(prompts_dict['instruction_property_final'], user_query, property_info, user_profile)
    response = get_chat_response(chat, prompt)
    return response


# chat function for property search
def chat_property(chat, prompts_dict, user_query, user_profile):
    # Fetch top properties from Zillow
    top_properties = get_listings_from_zillow(chat, prompts_dict, user_query)
    print('Top properties:', top_properties)
    # Use only property information(Add information if needed)
    property_info_final = top_properties
    # Generate the chatbot response using the user profile
    response_property_final = get_final_response_property(
        chat,
        prompts_dict,
        user_query,
        property_info=property_info_final,
        user_profile=user_profile
    )
    # Generate the property map
    map_html = create_property_map(api_key=GOOGLE_MAPS_API_KEY, top_properties=top_properties)  
    return response_property_final, map_html

# rewrite query to improve RAG performance(international student)
def rewrite_queries(chat, prompts_dict, user_query):
    prompt_rewrite_query = generate_prompt_rewrite_query(prompts_dict['instruction_rewrite_query'], user_query)
    response_rewrite_query = get_chat_response(chat, prompt_rewrite_query)
    print("Original Response from Rewrite Queries:", response_rewrite_query)

    try:
        # Attempt to parse the response content as JSON list
        result = json.loads(response_rewrite_query)

        # Check if result is a list and contains the original question and rewrites
        if isinstance(result, list) and user_query in result:
            return result
        else:
            # Return original question if parsing fails
            return [user_query]
    except (json.JSONDecodeError, AttributeError):
        # Return original question if there's an error
        return [user_query]


# chat function for international students
def chat_international(chat, prompts_dict, user_query, vectordb, user_profile, fusion=False):

    if fusion:
        rewritten_queries = rewrite_queries(chat, prompts_dict, user_query)
        all_results = []
        for query in rewritten_queries:
            chunks = search_similar_chunks(vectorstore=vectordb, query=query, k=5)
            all_results.append(chunks)
        chunks = reciprocal_rank_fusion(all_results, top_n=5)
    else:
        chunks = search_similar_chunks(vectorstore=vectordb, query=user_query, k=5)
    
    chunks_formated = format_chunk_results(
            chunks,
            metadata_fields=['source', 'source_type'],
            include_content=True
            )
    # print('Contexts:', chunks_formated)
    prompt_rag_international = generate_prompt_rag_international(prompts_dict['instruction_rag_international'], chunks_formated, user_query, user_profile)
    response_international_final = get_chat_response(chat, prompt_rag_international)
    return response_international_final


# chat function for general intent
def chat_general(chat, prompts_dict, user_query, user_profile):
    prompt_general = generate_prompt_general(prompts_dict['instruction_general'], user_query, user_profile)
    response_general_final = get_chat_response(chat, prompt_general)
    return response_general_final


# chat function for local advisor
def chat_local_advisor(chat, prompts_dict, user_query, api_key, user_profile):
    # Refine the user's query with LLM
    instruction = prompts_dict["instruction_local_advisor"]
    refined_query = generate_local_search_query(chat, instruction, user_query)

    search_string = refined_query["search_string"]
    included_type = refined_query["included_type"]

    # Perform the Google Places Text Search
    places = search_google_places(api_key, search_string, included_type)

    # Generate a response for the user using LLM
    if places:
        response_instruction = prompts_dict["instruction_local_advisor_response"]
        response = generate_local_advisor_response(chat, response_instruction, user_query, places, user_profile)
    else:
        response = f"Sorry, I couldn't find any results for '{search_string}'."

    # Step 4: Generate the map HTML
    map_html = create_local_advisor_map(api_key, places)

    return response, map_html


# main chat function based on user's intent
def chat_all(chat, prompts_dict, user_query, vectordb, user_profile):
    
    intent_int = intent_classifier(chat, prompts_dict, user_query)
    # Property intent
    if intent_int == 1:
        response_property_final, map_html = chat_property(chat, prompts_dict, user_query, user_profile)
        return response_property_final, map_html, intent_int
    # Local Advisor intent
    elif intent_int == 2:
        response_local_advisor, map_html = chat_local_advisor(chat, prompts_dict, user_query, GOOGLE_MAPS_API_KEY, user_profile)
        return response_local_advisor, map_html, intent_int
    # International Student Advisor intent
    elif intent_int == 3:
        response_international_final = chat_international(chat, prompts_dict, user_query, vectordb, user_profile, fusion=True)
        return response_international_final, None, intent_int
    # Other intent
    else:
        response_default = chat_general(chat, prompts_dict, user_query, user_profile)
        return response_default, None, intent_int
