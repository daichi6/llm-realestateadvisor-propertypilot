import os


def load_prompts(folder_path):
    """
    Reads all .txt files in the specified folder and stores their content in variables
    named after the files (excluding the .txt extension).

    :param folder_path: str - The path to the folder containing the .txt files.
    :return: dict - A dictionary where keys are file names without .txt extension and values are the content of the files.
    """
    file_contents = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            variable_name = filename[:-4]
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
                file_contents[variable_name] = file.read()

    return file_contents


def generate_prompt_classifier(instruction, user_query):
    """
    Generates a prompt for a classification task by replacing the user query placeholder.

    :param instruction: str - The instruction template containing a {USER_QUERY} placeholder.
    :param user_query: str - The user's original query.
    :return: str - The updated instruction with the {USER_QUERY} placeholder replaced by the user's query.
    """
    return instruction.replace("{USER_QUERY}", user_query)


def generate_prompt_property(instruction, user_query, property_info, user_profile):
    """
    Generates a prompt for a property query by replacing placeholders in the instruction with actual data.

    :param instruction: str - The instruction template containing placeholders.
    :param user_query: str - The user's original query.
    :param property_info: list - The detailed property information to include in the response.
    :param user_profile: dict - The user's profile information to include in the response.
    :return: str - The updated instruction with the placeholders replaced by the user query, property info, and key fields.
    """
    user_profile_str = "\n".join([f"{key}: {value}" for key, value in user_profile.items()])

    updated_instruction = instruction.replace("{USER_QUERY}", user_query)
    updated_instruction = updated_instruction.replace("{PROPERTY_INFO}", str(property_info))
    updated_instruction = updated_instruction.replace("{USER_PROFILE}", user_profile_str)
    return updated_instruction


def generate_prompt_apifilter(instruction, user_query, locations_string):
    """
    Generates a prompt by replacing the user query and locations string placeholders in the instruction.

    :param instruction: str - The instruction template containing placeholders for user query and locations.
    :param user_query: str - The user's original query.
    :param locations_string: str - The formatted string of locations to replace the {LOCATIONS_STRING} placeholder.
    :return: str - The updated instruction with both placeholders replaced.
    """
    zillow_prompt = instruction.replace("{USER_QUERY}", user_query)
    zillow_prompt = zillow_prompt.replace("{LOCATIONS_STRING}", locations_string)
    return zillow_prompt


def generate_prompt_rest_category(output_instructions, user_query, categories):
    """
    Generates a prompt by replacing the user query and categories string placeholders.

    :param user_query: str - The user's original query.
    :param categories: list - A list of categories to include in the prompt.
    :return: str - The updated instruction with the user query and categories inserted.
    """
    categories_string = ','.join(categories)
    updated_instruction = output_instructions.replace("{USER_QUERY}", user_query)
    updated_instruction = updated_instruction.replace("{CATEGORIES_STRING}", categories_string)
    return updated_instruction


def generate_prompt_rag_international(instruction, context, user_query, user_profile):
    """
    Replaces placeholders in the instruction template with the provided context and user query.

    :param instruction: str - The template instruction containing placeholders for context and user query.
    :param context: str - The context that will replace the {CONTEXT} placeholder in the instruction.
    :param user_query: str - The user query that will replace the {USER_QUERY} placeholder in the instruction.
    :param user_query: dict - User profile information
    :return: str - The updated instruction with the context and user query inserted.
    """

    user_profile_str = "\n".join([f"{key}: {value}" for key, value in user_profile.items()])
    instruction = instruction.replace("{USER_PROFILE}", user_profile_str)

    instruction = instruction.replace("{CONTEXT}", context)
    instruction = instruction.replace("{USER_QUERY}", user_query)
    return instruction 


def generate_prompt_rewrite_query(instructions, user_query):
    """
    Generates a prompt for rewriting queries by replacing placeholders with the user query.

    :param instructions: str - The template instruction containing a {USER_QUERY} placeholder.
    :param user_query: str - The user's original query.
    :return: str - The updated instruction with the {USER_QUERY} placeholder replaced.
    """
    updated_instruction = instructions.replace("{USER_QUERY}", user_query)
    return updated_instruction


def generate_prompt_local_advisor(instruction, user_query):
    """
    Generates a prompt for refining the user's query for Local Advisor.

    :param instruction: str - The instruction template containing placeholders for the query.
    :param user_query: str - The user's current query.
    :return: str - The instruction with the placeholder replaced by the user's query.
    """
    return instruction.replace("{USER_QUERY}", user_query)


def generate_prompt_local_advisor_response(instruction, user_query, places, user_profile):
    """
    Generates a prompt for the LLM to create a response for the Local Advisor.

    :param instruction: str - The instruction template containing placeholders.
    :param user_query: str - The user's query.
    :param places: list - A list of places from the Google Places API.
    :param user_profile: dict - User's profile information.
    :return: str - The prompt for the LLM.
    """
    # Convert the places list to a detailed string for inclusion in the prompt
    places_str = "\n".join(
        [
            f"Place {i+1}:\n" + "\n".join([f"  {key}: {value}" for key, value in place.items()])
            for i, place in enumerate(places[:5])  # Limit to 5 places
        ]
    )

    # Include user profile information in the prompt
    user_profile_str = "\n".join([f"{key}: {value}" for key, value in user_profile.items()])

    # Replace placeholders in the instruction
    prompt = instruction.replace("{USER_QUERY}", user_query)
    prompt = prompt.replace("{PLACES}", places_str)
    prompt = prompt.replace("{USER_PROFILE}", user_profile_str)

    return prompt


def generate_prompt_general(instruction, user_query, user_profile):
    """
    Generates the final output by replacing placeholders with the user query.

    :param instruction: str - The template instruction containing placeholders.
    :param user_query: str - The user's original query.
    :param user_profile: dict - User profile information to include in the response.
    :return: str - The updated instruction with the user query and user profile inserted.
    """
    user_profile_str = "\n".join([f"{key}: {value}" for key, value in user_profile.items()])
    instruction = instruction.replace("{USER_PROFILE}", user_profile_str)
    instruction = instruction.replace("{USER_QUERY}", user_query)
    return instruction
