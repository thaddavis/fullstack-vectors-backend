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