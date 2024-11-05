from property_info import extract_json_to_dict, fetch_top_properties_detail
from neighborhood import get_neighborhood_details
from property_info import extract_json_to_dict, fetch_top_properties_detail
from yelp import (
    yelp_advisor,
    fetch_top_businesses_near_properties,
    extract_business_info,
    merge_property_and_restaurant_info
)
from prompt_creation import (
    generate_prompt_classifier,
    generate_prompt_property,
    generate_prompt_apifilter,
    generate_prompt_rag_neighborhood,
    generate_prompt_yelp_advisor,
    final_output_yelp_advisor,
    generate_prompt_rag_international,
    generate_prompt_general
)
from llm import get_chat_response
from rag import get_context
from vector_search import search_similar_chunks, format_chunk_results


# initial intent
def intent_classifier(chat, prompts_dict, user_query):
    prompt = generate_prompt_classifier(prompts_dict['instruction_classifier'], user_query)
    response = get_chat_response(chat, prompt)
    print('Intent Number:', int(response))
    return int(response)


# functions for property search
def get_listings_from_zillow(chat, prompts_dict, user_query):
    prompt = generate_prompt_apifilter(prompts_dict['instruction_apifilter'], user_query, locations_string = prompts_dict['zillow_locations'])
    api_filter = get_chat_response(chat, prompt)
    api_filter = extract_json_to_dict(api_filter)
    top_properties = fetch_top_properties_detail(api_filter)
    return top_properties


def get_top_restaurants_yelp(chat, prompts_dict, user_query, top_properties):
    categories = prompts_dict['yelp_categories']
    yelp_results = fetch_top_businesses_near_properties(
        properties=top_properties,
        user_query=user_query,
        categories=categories,
        chat=chat,
        prompts_dict=prompts_dict
    )
    top_restaurants = extract_business_info(yelp_results)
    return top_restaurants
    

def get_final_respone_property(chat, prompts_dict, user_query, property_info):
    prompt = generate_prompt_property(prompts_dict['instruction_property_final'], user_query, property_info)
    response = get_chat_response(chat, prompt)
    return response
    

def chat_property(chat, prompts_dict, user_query, neighborhoods_info, neighborhoods_boundaries):
    top_properties = get_listings_from_zillow(chat, prompts_dict, user_query)
    print('Top properties:', top_properties)
    
    # Case1: Add Yelp and neighborhood information to the properties   
    # top_restaurants = get_top_restaurants_yelp(chat, prompts_dict, user_query, top_properties)
    # print('Top Restaurants:', top_restaurants)
    # top_properties_and_restaurants = merge_property_and_restaurant_info(top_properties, top_restaurants)
    # print('Top properties and restaurants:', top_properties_and_restaurants)
    # property_info_final = get_neighborhood_details(
    #     top_properties=top_properties_and_restaurants,
    #     neighborhoods_info=neighborhoods_info,
    #     neighborhoods_boundaries=neighborhoods_boundaries
    # )
    # print('Top properties and restaurants with Neighborhood info:', property_info_final)
    # response_property_final = get_final_respone_property(chat, prompts_dict, user_query, property_info=property_info_final)
    
    # Case2: Use only properties information
    property_info_final = top_properties
    response_property_final = get_final_respone_property(chat, prompts_dict, user_query, property_info=property_info_final)
    
    return response_property_final


# functions for restaurant search
def chat_yelp(chat, prompts_dict, user_query):
    categories_string = prompts_dict['yelp_categories']
    yelp_prompt = generate_prompt_yelp_advisor(prompts_dict['yelp_advisor_instructions'], user_query, categories_string)
    yelp_filter_str = get_chat_response(chat, yelp_prompt)
    yelp_filter = extract_json_to_dict(yelp_filter_str)
    yelp_advisor_results = yelp_advisor(yelp_filter)
    print('Yelp Info:', yelp_advisor_results)
    yelp_output_prompt = final_output_yelp_advisor(prompts_dict['yelp_output_instructions'], user_query, yelp_advisor_results)
    response_restaurant_final = get_chat_response(chat, yelp_output_prompt)
    return response_restaurant_final


# functions for neighborhood information
# def chat_neighborhood(chat, prompts_dict, user_query, vector_store):
#     context = get_context(user_query, vector_store)
#     print('Context:', context)
#     prompt_rag_neighborhood = generate_prompt_rag_neighborhood(prompts_dict['instruction_rag_neighborhood'], context, user_query)
#     response_neighborhood_final = get_chat_response(chat, prompt_rag_neighborhood)
#     return response_neighborhood_final


# functions for international students
def chat_international(chat, prompts_dict, user_query, vectordb):
    chunks = search_similar_chunks(vectorstore=vectordb, query=user_query, k=4)
    chunks_formated = format_chunk_results(
            chunks,
            metadata_fields=['source', 'source_type'],
            include_content=True
            )
    print('Contexts:', chunks_formated)
    prompt_rag_international = generate_prompt_rag_international(prompts_dict['instruction_rag_international'], chunks_formated, user_query)
    response_international_final = get_chat_response(chat, prompt_rag_international)
    return response_international_final


# functions for general response
def chat_general(chat, prompts_dict, user_query):
    prompt_general = generate_prompt_general(prompts_dict['instruction_general'], user_query)
    response_general_final = get_chat_response(chat, prompt_general)
    return response_general_final


# final
def chat_all(chat, prompts_dict, user_query, neighborhoods_info, neighborhoods_boundaries, vectordb):
    
    intent_int = intent_classifier(chat, prompts_dict, user_query)
    
    if intent_int == 1:
        return chat_property(chat, prompts_dict, user_query, neighborhoods_info, neighborhoods_boundaries), intent_int
    elif intent_int == 2:
        return chat_yelp(chat, prompts_dict, user_query), intent_int
    elif intent_int == 3:
        return chat_international(chat, prompts_dict, user_query, vectordb), intent_int
    else:
        return chat_general(chat, prompts_dict, user_query), intent_int