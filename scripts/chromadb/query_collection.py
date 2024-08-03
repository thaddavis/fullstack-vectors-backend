from typing import List
import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.HttpClient(host="chromadb", port=9000)
default_ef = embedding_functions.DefaultEmbeddingFunction()
print(chroma_client.list_collections())
collection = chroma_client.get_collection(name="rag_agent", embedding_function=default_ef)

query_vector: List[List[float]] = default_ef(["Tell me about Tad"])

results = collection.query(
    query_embeddings=[query_vector[0]],
    n_results=10
)

print()
print()
print('RESULTS:')
print()
print()

for r in results['metadatas'][0]:
    print(r['q'], '->', r['a'])

print()