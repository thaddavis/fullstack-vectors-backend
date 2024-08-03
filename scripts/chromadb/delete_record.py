import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.HttpClient(host="chromadb", port=9000)

default_ef = embedding_functions.DefaultEmbeddingFunction()

print(chroma_client.list_collections())

collection = chroma_client.get_collection(name="rag_agent", embedding_function=default_ef)

print('->', collection.count())

collection.delete(
    ids=["id1"]
)

print('->', collection.count())