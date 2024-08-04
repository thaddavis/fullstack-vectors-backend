import csv
from pinecone import Pinecone
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = "my-index"
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

print("BEFORE", index.describe_index_stats())

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

with open("./scratch/gptuesday_kb.csv") as kb_file:
    print(type(kb_file))

    csvreader = csv.reader(kb_file)

    header = next(csvreader)
    print(header)

    for row in csvreader:
        print('row')
        print('q:',row[0],'a:',row[1])

        embeddings = model.encode([row[0], row[1]])
        
        index.upsert(
          vectors=[
            # 1st index the question
            {
              "id": str(hash(row[0])),
              "values": embeddings[0],
              "metadata": {
                  "q": row[0],
                  "a": row[1],
                  "created_at": int(time.time())
                  
              },
            },
            # 2nd index the answer
            {
              "id": str(hash(row[1])),
              "values": embeddings[1],
              "metadata": {
                  "q": row[0],
                  "a": row[1],
                  "created_at": int(time.time())
              },
            },
          ]
        )        

print('Record count AFTER adding knowledge ->', index.describe_index_stats())
