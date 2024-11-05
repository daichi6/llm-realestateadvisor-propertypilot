import os
import pandas as pd
from llm import start_chat_session
from prompt_creation import load_prompts
from neighborhood import load_neighborhood_boundaries, load_neighborhood_info
from vector_search import load_vectordb

def setup():
    # Setup file path
    base_dir = os.path.dirname(__file__)
    prompts_path = os.path.join(base_dir, 'prompts')
    neighborhood_info_path = os.path.join(base_dir, 'data', 'neighborhood_info_final.csv')
    neighborhood_boundaries_path = os.path.join(base_dir, 'data', 'neighborhood_boundaries', 'geo_export_825d7df4-a9cd-4cef-b3d7-2ec1adc30204.shp')
    vectordb_path = os.path.join(base_dir, 'data', 'vectordb')

    # Chat setup
    chat = start_chat_session()
    # Load prompts
    prompts_dict = load_prompts(prompts_path)
    # Load neighborhood data
    neighborhoods_info = load_neighborhood_info(neighborhood_info_path)
    neighborhoods_boundaries = load_neighborhood_boundaries(neighborhood_boundaries_path)
    # Load vector store
    vectordb = load_vectordb(vectordb_path)

    return chat, prompts_dict, neighborhoods_info, neighborhoods_boundaries, vectordb


# Global Configuration
def configure_display_options():
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.width", None)