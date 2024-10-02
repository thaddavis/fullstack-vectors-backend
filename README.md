# TLDR

FastAPI for "Fullstack Vectors" course

## How to run the FastAPI

- pip install -r requirements.txt
- uvicorn src.main:app --host 0.0.0.0 --port 4000 --proxy-headers --reload

## How to save versions of top-level packages

- pip install pipreqs
- pipreqs . --force
