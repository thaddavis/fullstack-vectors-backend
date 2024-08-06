# TLDR

Info regarding PostgreSQL

- https://hub.docker.com/_/postgres
- docker run --network agent-network --name fullstack-pinecone -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
- psql -h 0.0.0.0 -p 5432 -U postgres

## Example Postgres connection string

- postgres://postgres:mysecretpassword@0.0.0.0:5432/mueshi_music

## Logging into the Postgres container √

- docker run -it --rm --network agent-network postgres psql -h fullstack-pinecone -U postgres
- create the db: `CREATE DATABASE fullstack_pinecone;`
