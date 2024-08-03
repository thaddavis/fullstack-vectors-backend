import csv
from typing import List
import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.HttpClient(host="chromadb", port=9000)
default_ef = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.get_collection(name="rag_agent", embedding_function=default_ef)

print('Record count BEFORE ->', collection.count())

with open("./scratch/kb.csv") as kb_file:
    print(type(kb_file))

    csvreader = csv.reader(kb_file)

    header = next(csvreader)
    print(header)

    for row in csvreader:
        print('row')
        print('q:',row[0],'a:',row[1])

        # 1st index the question

        collection.add(
            embeddings=[default_ef([row[0]])[0]],
            metadatas=[{"q": row[0],"a": row[1]}],
            ids=[str(hash(row[0]))]
        )

        # 2nd index the answer

        collection.add(
            embeddings=[default_ef([row[1]])[0]],
            metadatas=[{"q": row[0],"a": row[1]}],
            ids=[str(hash(row[1]))]
        )

print('Record count AFTER adding knowledge ->', collection.count())
