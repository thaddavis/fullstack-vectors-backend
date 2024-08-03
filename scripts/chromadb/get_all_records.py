import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.HttpClient(host="chromadb", port=9000)

default_ef = embedding_functions.DefaultEmbeddingFunction()

print(chroma_client.list_collections())

collection = chroma_client.get_collection(name="rag_agent", embedding_function=default_ef)

records = collection.get(include=['embeddings', 'metadatas'])

print('RECORDS:')

print(records)