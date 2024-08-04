from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")
embedding_dimensions = 384 # Depends on the embedding model you are using
pc = Pinecone(api_key=api_key)

pc.create_index(
    name=index_name,
    dimension=embedding_dimensions, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)