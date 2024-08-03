import chromadb

chroma_client = chromadb.HttpClient(host="chromadb", port=9000)

print(chroma_client.list_collections())

collections = chroma_client.list_collections()

c_name = "rag_agent"
c_exists = False
for c in collections:
    print(c)
    print(c.name)
    if (c.name == c_name):
        c_exists = True
        break

if not c_exists:
    chroma_client.create_collection(name=c_name)
    print(chroma_client.list_collections())
else:
    print(f'Collection "{c_name}" already exists')
