import chromadb

chroma_client = chromadb.HttpClient(host="chromadb", port=9000)

collection = chroma_client.get_collection(name="rag_agent")

print('->', collection.count())