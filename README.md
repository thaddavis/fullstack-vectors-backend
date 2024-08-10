# TLDR

FastAPI for "Fullstack R.A.G." course

## How to run the FastAPI

- pip install -r requirements.txt
- uvicorn src.main:app --host 0.0.0.0 --port 4000 --proxy-headers --reload

## ChromaDB - setting up the container

- NOTE: make sure `agent-network` is created
      - `docker network ls`
      - `docker network create -d bridge agent-network`
- git clone https://github.com/chroma-core/chroma
    - cd chroma
- docker build -f Dockerfile -t chromadb .
- docker run --network agent-network --name chromadb -p 8000:8000 -d chromadb
- docker inspect --format='{{json .NetworkSettings.Networks}}' chromadb | jq

## ChromaDB - creating a collection

- python scripts/chromadb/create_collection.py √

## Chroma DB - how to seed a collection with Q&A's

- python scripts/chromadb/add_csv_records.py √

## Redis - setting up the container

- docker run --network agent-network --name agent-memory -p 6739:6739 -d redis

## How to save versions of top-level packages

- pip install pipreqs
- pipreqs . --force

