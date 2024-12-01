import os
import pandas as pd
from llm import start_chat_session
from prompt_creation import load_prompts
from vector_search import load_vectordb

def setup():
    # Setup file path
    base_dir = os.path.dirname(__file__)
    prompts_path = os.path.join(base_dir, 'prompts')
    vectordb_path = os.path.join(base_dir, 'data', 'vectordb')

    # Chat setup
    chat = start_chat_session()
    # Load prompts
    prompts_dict = load_prompts(prompts_path)
    # Load vector store
    vectordb = load_vectordb(vectordb_path)

    return chat, prompts_dict, vectordb


# Global Configuration
def configure_display_options():
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.width", None)