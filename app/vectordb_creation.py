from typing import List, Dict, Tuple
from datetime import datetime
from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urlparse
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict, Optional
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables")

def fetch_web_content(url: str, verify_ssl: bool = True, timeout: int = 10) -> str:
    """
    Fetch content from a single URL.
    """
    response = requests.get(url, verify=verify_ssl, timeout=timeout)
    response.raise_for_status()
    return response.text

def extract_metadata(url: str, html_content: str) -> Dict:
    """
    Extract metadata from HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    metadata = {
        "source": url,
        "domain": urlparse(url).netloc,
        "fetch_date": datetime.now().isoformat(),
        "content_type": "web_page"
    }
    
    # Extract meta tags
    if soup.title:
        metadata["title"] = soup.title.string
        
    for meta in soup.find_all('meta'):
        name = meta.get('name', '').lower()
        property = meta.get('property', '').lower()
        content = meta.get('content')
        
        if name == 'description' or property == 'og:description':
            metadata['description'] = content
        elif name == 'keywords':
            metadata['keywords'] = content
        elif name == 'author':
            metadata['author'] = content
            
    return metadata

def clean_content(html_content: str) -> str:
    """
    Clean and extract main content from HTML.
    """
    return trafilatura.extract(html_content) or ""

def create_document(url: str, verify_ssl: bool = True) -> Document:
    """
    Create a single document from a URL.
    """
    try:
        html_content = fetch_web_content(url, verify_ssl)
        metadata = extract_metadata(url, html_content)
        cleaned_content = clean_content(html_content)
        
        return Document(
            page_content=cleaned_content,
            metadata=metadata
        )
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None

def split_document(doc: Document, 
                  chunk_size: int = 1000, 
                  chunk_overlap: int = 200) -> List[Document]:
    """
    Split a document into chunks.
    """
    if not doc:
        return []
        
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_documents([doc])
    
    # Add chunk metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            "chunk_index": i,
            "total_chunks": len(chunks),
            "chunk_size": len(chunk.page_content)
        })
    
    return chunks

def process_urls(urls: List[str], 
                chunk_size: int = 1000, 
                chunk_overlap: int = 200, 
                verify_ssl: bool = True) -> List[Document]:
    """
    Main function to process multiple URLs into chunked documents.
    """
    all_chunks = []
    
    for url in urls:
        # Create document from URL
        doc = create_document(url, verify_ssl)
        if doc:
            # Split into chunks
            chunks = split_document(doc, chunk_size, chunk_overlap)
            all_chunks.extend(chunks)
    
    return all_chunks


def enhance_metadata(documents: List[Document]) -> List[Document]:
    """
    Enhance metadata of documents with additional classifications.
    Currently adds source_type for uchicago domains.
    
    Args:
        documents: List of Document objects to enhance
    
    Returns:
        List of Documents with enhanced metadata
    """
    enhanced_docs = []
    for doc in documents:
        # Create a copy of the document to avoid modifying the original
        new_doc = Document(
            page_content=doc.page_content,
            metadata=doc.metadata.copy()
        )
        
        # Check domain for uchicago
        if 'domain' in new_doc.metadata:
            if 'uchicago' in new_doc.metadata['domain'].lower():
                new_doc.metadata['source_type'] = 'uchicago'
        
        enhanced_docs.append(new_doc)
    
    return enhanced_docs


def init_embeddings(model: str = "text-embedding-3-small") -> OpenAIEmbeddings:
    """
    Initialize OpenAI embeddings model.
    
    Args:
        model: Name of the OpenAI embedding model to use
    
    Returns:
        OpenAIEmbeddings instance configured with the specified model
    """
    return OpenAIEmbeddings(
        openai_api_key=openai_api_key,
        model=model
    )


def create_and_save_vectordb(documents: List[Document], 
                           embeddings: OpenAIEmbeddings,
                           save_path: Optional[str] = None) -> FAISS:
    """
    Create FAISS vector database from documents and optionally save it.
    
    Args:
        documents: List of Document objects to create embeddings for
        embeddings: Configured OpenAI embeddings model instance
        save_path: Optional path to save the vector database
    
    Returns:
        FAISS vector store object
    """
    if not documents:
        print("Error: Document list is empty")
        return None
        
    try:
        print("Creating vector store...")
        vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=embeddings
        )
        print("Vector store created successfully")
        
        if save_path:
            os.makedirs(save_path, exist_ok=True)
            print(f"Saving vector database to {save_path}...")
            vectorstore.save_local(save_path)
            print(f"Vector database saved successfully to {save_path}")
            
        return vectorstore
        
    except Exception as e:
        print(f"Error occurred while creating vector store: {str(e)}")
        return None


def main():

    urls = [
    "https://internationalaffairs.uchicago.edu/page/health-and-safety",
    "https://internationalaffairs.uchicago.edu/ssn",
    "https://internationalaffairs.uchicago.edu/itin",
    "https://internationalaffairs.uchicago.edu/page/tax-responsibilities-international-students-and-scholars",
    "https://internationalaffairs.uchicago.edu/page/transportation",
    "https://internationalaffairs.uchicago.edu/page/beware-scams",
    "https://internationalaffairs.uchicago.edu/page/understanding-f-1-and-j-1-visas",
    "https://internationalaffairs.uchicago.edu/frs",
    "https://internationalaffairs.uchicago.edu/page/financial-documentation-requirements",
    "https://internationalaffairs.uchicago.edu/transferin",
    "https://internationalaffairs.uchicago.edu/fmjfee",
    "https://internationalaffairs.uchicago.edu/page/requesting-visa",
    "https://internationalaffairs.uchicago.edu/page/changing-status-us",
    "https://internationalaffairs.uchicago.edu/page/arriving-us",
    "https://internationalaffairs.uchicago.edu/page/otherstatus",
    "https://wellness.uchicago.edu/medical-services/immunizations/",
    "https://wellness.uchicago.edu/student-insurance/u-ship/faqs-and-other-resources/",
    "https://grad.uchicago.edu/life-at-uchicago/housing/getting-started/roommates/",
    "https://grad.uchicago.edu/life-at-uchicago/housing/getting-started/information-for-individuals-with-disabilities/",
    "https://grad.uchicago.edu/life-at-uchicago/housing/getting-started/tips-for-families-with-children/",
    "https://grad.uchicago.edu/life-at-uchicago/housing/finding-an-apartment/",
    "https://grad.uchicago.edu/life-at-uchicago/housing/finding-an-apartment/other-chicago-neighborhoods/",
    "https://grad.uchicago.edu/life-at-uchicago/housing/finding-an-apartment/apartment-listings/"
    ]

     # Process URLs
    documents = process_urls(
        urls=urls,
        chunk_size=2000,
        chunk_overlap=200
    )
    
    print(f"\nInitial processing:")
    print(f"Processed {len(documents)} chunks from {len(urls)} URLs")
    
    # Enhance metadata
    enhanced_docs = enhance_metadata(documents)
    print("\nMetadata enhancement complete")

    # Initialize embeddings
    embeddings = init_embeddings()
    
    # Create and save vector database
    base_dir = os.path.dirname(__file__)
    vectordb = create_and_save_vectordb(
        documents=enhanced_docs,
        embeddings=embeddings,
        save_path=os.path.join(base_dir, 'data', 'vectordb')
    )
    print("\nVector database creation complete")
    

    print("\nExample of enhanced documents:")
    for i, doc in enumerate(enhanced_docs[:2]):
        print(f"\nChunk {i+1}:")
        print("Enhanced Metadata:", doc.metadata)
        print("Content preview:", doc.page_content[:200], "...")

if __name__ == "__main__":
    main()