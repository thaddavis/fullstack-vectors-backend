# TLDR

Useful info related to https://www.pinecone.io/

## Documenting process

- Signing up / Logging into [Pinecone](https://www.pinecone.io/)
- Where are going to be starting with a `Starter` (aka Free) Pinecone account
- If you need more capacity then Pinecone also offers a `Standard` and `Enterprise` plan

## Notes on Pinecone's organizational hierarchy

- Organizations > Projects > Index > Namespace > Record
- ALSO NOTE: A Pinecone "collection" is a snapshot of an Index.

## Getting set up with Pinecone

- Create a project called `rag-with-pinecone`
- Install the pinecone-client
  - https://pypi.org/project/pinecone-client/
  - add `pinecone-client>=5.0.1,<6.0` to the requirements.txt file
- Create an API key

## Create an index (ie: a Pinecone database) where we'll store our data

- python scripts/pinecone/create_index.py

## Test adding a record to the index with `sentence-transformers`

- https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
  - Creates embeddings with 384 dimensions
- python scripts/pinecone/add_record.py

## Upload .csv of QnA's to seed the Pinecone Index

- CHECK OUT: `data/gptuesday_kb.csv`
- python scripts/pinecone/add_csv_records.py

## Add Pinecone similarity search to the R.A.G. agent

- CHECK OUT: `src/_4_ragAgent/router.py`
- https://docs.pinecone.io/guides/data/query-data#using-metadata-filters-in-queries

