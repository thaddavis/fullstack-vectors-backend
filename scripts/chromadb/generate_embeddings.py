from typing import List
from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()

val: List[List[float]] = default_ef(["Tad", "Duval"])

print(f"Embeddings count: {len(val)}")
print(f"Embedding dimensions: {len(val[0])}")