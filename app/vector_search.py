from typing import List, Dict, Optional
from langchain.schema import Document
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.load import dumps, loads


load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables")


def load_vectordb(load_path: str, model: str = "text-embedding-3-small") -> FAISS:
    """
    Load FAISS vector database from disk using OpenAI embeddings.

    :param load_path: str - Path where the database is stored.
    :param model: str - OpenAI embedding model name (default: "text-embedding-3-small").
    :return: FAISS - Vector store object.
    """
    try:
        # Initialize OpenAI embedding model
        embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key,
            model=model
        )
        
        # Load vector store
        vectorstore = FAISS.load_local(
            folder_path=load_path,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore
    except Exception as e:
        print(f"Error loading vector database: {str(e)}")
        return None


def search_similar_chunks(vectorstore: FAISS,
                         query: str,
                         k: int = 5,
                         filter_dict: Optional[Dict] = None) -> List[Document]:
    """
    Search for similar chunks in the vector database.

    :param vectorstore: FAISS - FAISS vector store instance.
    :param query: str - Search query string.
    :param k: int - Number of similar chunks to return (default: 5).
    :param filter_dict: Optional[Dict] - Optional metadata filters (e.g., {"source_type": "uchicago"}).
    :return: List[Document] - List of similar Document objects.
    """
    try:
        if filter_dict:
            similar_docs = vectorstore.similarity_search(
                query,
                k=k,
                filter=filter_dict
            )
        else:
            similar_docs = vectorstore.similarity_search(
                query,
                k=k
            )
        return similar_docs
    
    except Exception as e:
        print(f"Error during similarity search: {str(e)}")
        return []


def format_chunk_results(documents: List[Document],
                         metadata_fields: Optional[List[str]] = None,
                         include_content: bool = True,
                         max_content_length: Optional[int] = None) -> str:
    """
    Format search results into a readable string.

    :param documents: List[Document] - List of Document objects from search results.
    :param metadata_fields: Optional[List[str]] - List of metadata fields to include (None for all fields).
    :param include_content: bool - Whether to include the content in the output (default: True).
    :param max_content_length: Optional[int] - Maximum length of content to display (None for full content).
    :return: str - Formatted string of search results.
    """
    if not documents:
        return "No results found."
    
    # Default metadata fields if none specified
    default_fields = ['source', 'domain', 'source_type', 'chunk_index', 'total_chunks']
    metadata_fields = metadata_fields or default_fields
    
    output_parts = []
    output_parts.append(f"Found {len(documents)} relevant chunks:\n")
    
    for i, doc in enumerate(documents, 1):
        # Add chunk header
        output_parts.append(f"\nChunk {i}:")
        output_parts.append("-" * 10)
        
        # Add metadata
        metadata_lines = []
        for field in metadata_fields:
            if field in doc.metadata:
                value = doc.metadata[field]
                # Format the field name for display
                display_field = field.replace('_', ' ').title()
                metadata_lines.append(f"{display_field}: {value}")
        output_parts.append('\n'.join(metadata_lines))
        
        # Add content if requested
        if include_content:
            output_parts.append("\nContent:")
            output_parts.append("-" * 10)
            content = doc.page_content
            if max_content_length and len(content) > max_content_length:
                content = content[:max_content_length] + "..."
            output_parts.append(content)
            output_parts.append("-" * 10)
    
    return '\n'.join(output_parts)


def reciprocal_rank_fusion(results: list[list], k=60, top_n=5):
    """
    Perform reciprocal rank fusion for merging multiple lists of ranked documents.
    Returns only the top_n documents.

    :param results: list[list] - Lists of ranked documents to merge.
    :param k: int - Smoothing factor for rank scores (default: 60).
    :param top_n: int - Number of top-ranked documents to return (default: 5).
    :return: list - Merged and reranked list of top_n documents.
    """
    fused_scores = {}

    for docs in results:
        for rank, doc in enumerate(docs):
            # Serialize doc to use as a dictionary key
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)
        
    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    # Return only the top_n documents
    return [doc for doc, score in reranked_results[:top_n]]