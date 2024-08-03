from typing import List
import chromadb

from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()

chroma_client = chromadb.HttpClient(host="chromadb", port=9000)

print("LIST COLLECTIONS")
print(chroma_client.list_collections())

collection = chroma_client.get_collection(name="rag_agent", embedding_function=default_ef)

val: List[List[float]] = default_ef(["Who is the president?"])

collection.add(
    embeddings=[val[0]],
    metadatas=[{"q": "Who is the president?","a": "Tad Duval"}],
    ids=["id1"]
)