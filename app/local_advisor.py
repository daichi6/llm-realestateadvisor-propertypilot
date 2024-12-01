import requests
from llm import get_chat_response
from prompt_creation import generate_prompt_local_advisor, generate_prompt_local_advisor_response
from property_info import extract_json_to_dict


def generate_local_search_query(chat, instruction, user_query):
    """
    Refines the user's query for Local Advisor using LLM.

    :param chat: object - The chat instance for interacting with the LLM.
    :param instruction: str - Instruction template for the LLM.
    :param user_query: str - The user's query to refine.
    :return: dict - A JSON object with "search_string" and "included_type" fields.
    """
    prompt = generate_prompt_local_advisor(instruction, user_query)
    response = get_chat_response(chat, prompt)

    # Extract and parse the JSON from the response
    refined_query = extract_json_to_dict(response)
    if isinstance(refined_query, str):
        raise ValueError(f"Invalid JSON response from LLM: {response}")

    return refined_query


def search_google_places(api_key, search_string, included_type):
    """
    Performs a Google Places Text Search (New) based on the provided parameters.

    :param api_key: str - Your Google Maps API key.
    :param search_string: str - The search query for the Places API (e.g., "pizza in New York").
    :param included_type: str - The most relevant type for the search (e.g., "restaurant").
    :return: list - A list of results (place details) from the Google Places API.
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    # Default location bias set to Chicago coordinates
    location = {"lat": 41.8781, "lng": -87.6298}
    radius = 50000

    # Construct the parameters
    params = {
        "query": search_string,
        "key": api_key,
        "type": included_type,
        "region": "us",
        "language": "en-US",
        "location": f"{location['lat']},{location['lng']}",
        "radius": radius
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Handle the response
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            results = data["results"]
            
            # Add Google Maps link for each result
            for result in results:
                place_id = result.get("place_id")
                if place_id:
                    result["google_maps_link"] = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            
            print(results)  # Debug: Check the results with added links
            return results
        else:
            print("No results found.")
            return []
    else:
        raise ValueError(f"Google Places API error: {response.status_code} {response.text}")


def generate_local_advisor_response(chat, instruction, user_query, places, user_profile):
    """
    Generates a response for the Local Advisor using LLM.

    :param chat: object - The chat instance for interacting with the LLM.
    :param instruction: str - Instruction template for the LLM.
    :param user_query: str - The user's query.
    :param places: list - A list of places from the Google Places API.
    :param user_profile: dict - The user's profile information.
    :return: str - The generated response from the LLM.
    """
    prompt = generate_prompt_local_advisor_response(instruction, user_query, places, user_profile)
    response = get_chat_response(chat, prompt)
    return response