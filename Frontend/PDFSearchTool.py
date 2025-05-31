from crewai_tools import PDFSearchTool

# Initialize the tool with a specific PDF path and custom configuration
tool = PDFSearchTool(
    pdf='C:\\Users\\Ananya\\Desktop\\Hackathon_Project\\Data\\MSR Sample Active Substance Use 2023.pdf',  # Path to your PDF file
    config=dict(
        llm=dict(
            provider="ollama",  # Use Ollama as the LLM provider
            config=dict(
                model="llama2",  # Use the Llama2 model
                temperature=0.5,  # Adjust creativity (0 = deterministic, 1 = creative)
                top_p=1,  # Controls diversity of responses
                stream=True,  # Stream responses (useful for real-time applications)
            ),
        ),
        embedder=dict(
            provider="google",  # Use Google's embedding model
            config=dict(
                model="models/embedding-001",  # Specify the embedding model
                task_type="retrieval_document",  # Task type for embeddings
            ),
        ),
    )
)

# Example query
query = "What are the key findings in this document?"
result = tool.search(query)  # Perform the search
print(result)