import http.client
import json
import urllib.parse
from typing import Dict, Any
import os
from llm import get_chat_response
from prompt_creation import generate_prompt_rest_category
from dotenv import load_dotenv
load_dotenv()


yelp_api = os.getenv("YELP_API_KEY")


def yelp_advisor(yelp_filter, api_key=yelp_api):
    """
    Fetches top-rated businesses near a given location from Yelp.

    :param api_key: str - The API key for accessing Yelp's API.
    :param yelp_filter: Dict[str, Any] - A dictionary of filters to apply to the Yelp search (e.g., location, category, radius).
    :return: dict or None - A dictionary containing the Yelp API response data, or None if the request fails.
    """
    conn = http.client.HTTPSConnection("api.yelp.com")
    
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    params = yelp_filter
    
    # Encode parameters into URL query string
    query_string = urllib.parse.urlencode(params, doseq=True)
    #print(query_string)
    url = f"/v3/businesses/search?{query_string}"
    
    conn.request("GET", url, headers=headers)
    
    response = conn.getresponse()
    data = response.read()
    conn.close()
    
    if response.status == 200:
        return json.loads(data)
    else:
        print(f"Failed to fetch data: {response.status} - {data.decode('utf-8')}")
        return None

    
def get_top_rated_businesses(location, category, top_n=2, api_key=yelp_api):
    """
    Fetches top-rated businesses near a given location from Yelp.

    :param api_key: str - The API key for accessing Yelp's API.
    :param location: str - The latitude and longitude of the location (formatted as 'latitude,longitude').
    :param category: str - The business category to search for (e.g., 'restaurants', 'bars').
    :param top_n: int - The number of top businesses to return (default is 2).
    :return: dict or None - A dictionary of businesses if the request is successful, otherwise None.
    """
    conn = http.client.HTTPSConnection("api.yelp.com")
    
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    params = {
        'location': location,
        'term': 'restaurants',
        'radius': 2000,
        'categories': category,
        'sort_by': 'rating',
        'limit': top_n
    }
    
    # Encode parameters into URL query string
    query_string = urllib.parse.urlencode(params)
    url = f"/v3/businesses/search?{query_string}"
    
    conn.request("GET", url, headers=headers)
    
    response = conn.getresponse()
    data = response.read()
    conn.close()
    
    if response.status == 200:
        return json.loads(data)
    else:
        print(f"Failed to fetch data: {response.status} - {data.decode('utf-8')}")
        return None  # Handle the failure as appropriate in your application


# properties - this should be address information in the future
def fetch_top_businesses_near_properties(properties, user_query, categories, chat, prompts_dict):
    """
    Fetches top-rated businesses of a specified category near each property in a given list,
    using a category inferred from a user query processed by Gemini LLM.

    :param api_key: str - The API key for accessing Yelp's API.
    :param properties: list - A list of properties, each containing latitude, longitude, and address information.
    :param user_query: str - The query from the user to infer the desired business category.
    :param categories: str - Possible categories to assist the LLM in understanding the query.
    :param chat: ChatSession - The active chat session with the generative model.
    :return: list - A list of dictionaries, each containing an address and the top businesses near it.
    """
    prompt = generate_prompt_rest_category(prompts_dict['instruction_rest_category'], user_query, categories)
    category = get_chat_response(chat, prompt)  # Get the category from the LLM
    category = category.strip().replace('"', '')  # Strip any quotation marks or white space from the category
    if not category or category.lower() == "restaurants":
        category = "restaurants"  # default to 'restaurants' if no specific category identified

    top_restaurants_yelp = []
    for property in properties:
        location = f"{property['latitude']}, {property['longitude']}"
        top_businesses = get_top_rated_businesses(location, category)
        top_restaurants_yelp.append({
            'address': property['address'],
            'top_businesses': top_businesses
        })
    
    return top_restaurants_yelp


def extract_business_info(addresses, n=2, fields=['business_name', 'categories_titles', 'rating', 'latitude', 'longitude', 'display_address', 'url']):
    """
    Extracts and returns information from a given list of addresses, each containing businesses,
    based on the specified fields and the top 'n' businesses per address.

    :param addresses: list - A list of dictionaries, each representing an address with nested businesses.
    :param n: int - The number of top businesses to extract from each address.
    :param fields: list - A list of strings representing the fields to extract from each business.
    :return: list - A list of dictionaries, each representing a business with only the specified fields.
    """
    extracted_businesses = []
    try:
        # Loop through each address entry
        for address_entry in addresses:
            # Extract top 'n' businesses
            for business in address_entry['top_businesses']['businesses'][:n]:
                # Extract specified fields, handling nested structures like 'categories' and 'location'
                extracted_business = {
                    'business_name': business.get('name'),
                    'categories_titles': [category['title'] for category in business.get('categories', [])],
                    'rating': business.get('rating'),
                    'latitude': business.get('coordinates', {}).get('latitude'),
                    'longitude': business.get('coordinates', {}).get('longitude'),
                    'display_address': " ".join(business.get('location', {}).get('display_address', [])),
                    'url': business.get('url')
                }
                # Only append fields that were specifically requested
                filtered_business = {field: extracted_business[field] for field in fields if field in extracted_business}
                extracted_businesses.append(filtered_business)

        return extracted_businesses

    except Exception as e:
        print("An error occurred:", e)
        return []

    
def merge_property_and_restaurant_info(properties, restaurants):
    """
    Merges property data with restaurant information for each property.

    :param properties: list - A list of property dictionaries.
    :param restaurants: list - A list of restaurant dictionaries.
    :return: list - A list of merged property and restaurant dictionaries.
    """
    # Ensure there are two restaurants for each property, assuming a structure of 1:2 mapping
    if len(restaurants) != 2 * len(properties):
        raise ValueError("Each property must correspond to exactly two restaurants.")

    merged_data = []
    for i, property in enumerate(properties):
        # Merge the property dict with its corresponding restaurants' info
        restaurant_info = {
            "restaurant_1": restaurants[2*i],
            "restaurant_2": restaurants[2*i + 1]
        }
        # Merge two dictionaries and add to the list
        merged_property = {**property, **restaurant_info}
        merged_data.append(merged_property)

    return merged_data