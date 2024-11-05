import os


def load_prompts(folder_path):
    """
    Reads all .txt files in the specified folder and stores their content in variables
    named after the files (excluding the .txt extension).

    Parameters:
    folder_path (str): The path to the folder containing the .txt files.

    Returns:
    dict: A dictionary where keys are file names without .txt extension and values are the content of the files.
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


def generate_prompt_property(instruction, user_query, property_info):
    """
    Generates a prompt for a property query by replacing placeholders in the instruction with actual data.

    :param instruction: str - The instruction template containing placeholders.
    :param user_query: str - The user's original query.
    :param property_info: list - The detailed property information to include in the response. It can also include local information.
    :return: str - The updated instruction with the placeholders replaced by the user query, property info, and key fields.
    """
    updated_instruction = instruction.replace("{USER_QUERY}", user_query)
    updated_instruction = updated_instruction.replace("{PROPERTY_INFO}", str(property_info))
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


def generate_prompt_rag_neighborhood(instruction, context, user_query):
    """
    Replaces placeholders in the instruction template with the provided context and user query.

    :param instruction: str - The template instruction containing placeholders for context and user query.
    :param context: str - The context that will replace the {CONTEXT} placeholder in the instruction.
    :param user_query: str - The user query that will replace the {USER_QUERY} placeholder in the instruction.
    :return: str - The updated instruction with the context and user query inserted.
    """
    instruction = instruction.replace("{CONTEXT}", context)
    return instruction.replace("{USER_QUERY}", user_query)


def generate_prompt_rag_international(instruction, context, user_query):
    """
    Replaces placeholders in the instruction template with the provided context and user query.

    :param instruction: str - The template instruction containing placeholders for context and user query.
    :param context: str - The context that will replace the {CONTEXT} placeholder in the instruction.
    :param user_query: str - The user query that will replace the {USER_QUERY} placeholder in the instruction.
    :return: str - The updated instruction with the context and user query inserted.
    """
    instruction = instruction.replace("{CONTEXT}", context)
    return instruction.replace("{USER_QUERY}", user_query)


def generate_prompt_yelp_advisor(yelp_advisor_instruction, user_query, categories_string):
    """
    Generates a Yelp advisor prompt by replacing the user query and categories string placeholders.

    :param yelp_advisor_instruction: str - The instruction template containing placeholders for user query and categories.
    :param user_query: str - The user's original query.
    :param categories_string: str - The string of business categories to replace the {CATEGORIES_STRING} placeholder.
    :return: str - The updated instruction with the user query and categories inserted.
    """
    prompt = yelp_advisor_instruction.replace("{USER_QUERY}", user_query)
    prompt = prompt.replace("{CATEGORIES_STRING}", categories_string)
    return prompt


def final_output_yelp_advisor(output_instructions, user_query, yelp_advisor_results):
    """
    Generates the final output by replacing placeholders with the user query and Yelp results.

    :param output_instructions: str - The template instruction for the output.
    :param user_query: str - The user's original query.
    :param yelp_advisor_results: dict - The results from the Yelp advisor.
    :return: str - The updated instruction with the user query and Yelp results inserted.
    """
    updated_instruction = output_instructions.replace("{USER_QUERY}", user_query)
    updated_instruction = updated_instruction.replace("{YELP_RESULTS}", str(yelp_advisor_results))
    return updated_instruction


def generate_prompt_rest_category(output_instructions, user_query, categories):
    """
    Generates a prompt by replacing the user query and categories string placeholders.

    :param user_query: str - The user's original query.
    :param categories: list - A list of categories to include in the prompt.
    :return: str - The updated instruction with the user query and categories inserted.
    """
    # Format the list into a single string separated by commas for the model
    categories_string = ','.join(categories)
    updated_instruction = output_instructions.replace("{USER_QUERY}", user_query)
    updated_instruction = updated_instruction.replace("{CATEGORIES_STRING}", categories_string)
    return updated_instruction


def generate_prompt_general(instructions, user_query):
    """
    Generates the final output by replacing placeholders with the user query.
    """
    updated_instruction = instructions.replace("{USER_QUERY}", user_query)
    return updated_instruction