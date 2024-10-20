import os
import pandas as pd
import numpy as np
import numpy.linalg
from google.api_core import retry
from vertexai.language_models import TextEmbeddingModel


embeddings_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")


def load_vector_store(file_path):
    """
    Loads the vector store from a CSV file, converting the 'embeddings' column into numpy arrays.

    :param file_path: str - Path to the CSV file containing the vector store.
    :return: pd.DataFrame - DataFrame with 'embeddings' as numpy arrays.
    """
    vector_store = pd.read_csv(file_path)
    # Convert the 'embeddings' column to numpy arrays
    vector_store['embeddings'] = vector_store['embeddings'].apply(lambda x: np.array(list(map(float, x.split(',')))))

    return vector_store


# Compute the cosine similarity of two vectors, wrap as returned function to make easier to use with Pandas
def get_similarity_fn(query_vector):
    """
    Creates a function to compute the cosine similarity between a query vector and row vectors from a DataFrame.

    :param query_vector: np.array - The embedding vector representing the search query.
    :return: function - A function that computes the cosine similarity between the query vector and a DataFrame row.
    """
    def fn(row):
        return np.dot(row, query_vector) / (
            numpy.linalg.norm(row) * numpy.linalg.norm(query_vector)
        )

    return fn


@retry.Retry(timeout=300.0)
def get_embeddings(text):
    """
    Fetches the embedding vector for the given text using a pre-trained model, with retry logic for robustness.

    :param text: str - The text to be embedded.
    :return: np.array - The embedding vector for the provided text.
    """
    return embeddings_model.get_embeddings([text])[0].values


def get_context(question, vector_store, num_docs=10):
    """
    Retrieves the most relevant context by finding the top-matching documents in a vector store.

    :param question: str - The query or question to be embedded and compared against stored embeddings.
    :param vector_store: pd.DataFrame - A DataFrame containing text and embedding vectors for documents.
    :param num_docs: int - The number of top-matching documents to retrieve.
    :return: str - A concatenated string of the top-matching documents' text.
    """
    # Embed the search query
    query_vector = np.array(get_embeddings(question))

    # Get similarity to all other vectors and sort, cut off at num_docs
    top_matched = (
        vector_store["embeddings"]
        .apply(get_similarity_fn(query_vector))
        .sort_values(ascending=False)[:num_docs]
        .index
    )
    top_matched_df = vector_store[vector_store.index.isin(top_matched)][["texts"]]

    # Return a string with the top matches
    context = " ".join(top_matched_df.texts.values)
    return context