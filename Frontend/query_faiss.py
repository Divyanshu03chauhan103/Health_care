from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings  # Updated import

# Initialize Hugging Face Embeddings
model_name = "sentence-transformers/all-MiniLM-L6-v2"
huggingface_embeddings = HuggingFaceEmbeddings(model_name=model_name)

# Load FAISS Index with Hugging Face Embeddings
vector_store = FAISS.load_local(
    r"C:\Users\Divyanshu\Desktop\ML projects\HealthCareSystem\faiss_index",  # Path to the FAISS index
    embeddings=huggingface_embeddings,
    allow_dangerous_deserialization=True  # Allow loading of pickle files
)

# Function to Query FAISS
def query_faiss(query):
    """
    Query the FAISS vector store and return the top 3 matches.

    Args:
        query (str): The query string to search for.

    Returns:
        list: A list of the top 3 matching documents (as strings).
    """
    # Generate query embedding
    query_embedding = huggingface_embeddings.embed_query(query)
    
    # Perform similarity search
    results = vector_store.similarity_search_by_vector(query_embedding, k=3)
    
    # Return results as a list of strings
    return [doc.page_content for doc in results]