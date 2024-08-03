import chromadb

chroma_client = chromadb.HttpClient(host="chromadb", port=9000)

print(chroma_client.list_collections())

collection = chroma_client.delete_collection(name="rag_agent")

print(chroma_client.list_collections())