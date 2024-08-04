from pinecone import Pinecone
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

print("BEFORE", index.describe_index_stats())

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
chunks = [{
 "q": "What is GPTuesday?",
 "a": "A Miami-based AI meetup that takes place every Tuesday at Office Logic."
}]
embeddings = model.encode([chunks[0]['q'], chunks[0]['a']])
print(embeddings)

index.upsert(
  vectors=[
    {
      "id": str(hash(chunks[0]['q'])),
      "values": embeddings[0],
      "metadata": {"q": chunks[0]['q'], "a": chunks[0]['a']}
    },
  ]
)

print("AFTER", index.describe_index_stats())