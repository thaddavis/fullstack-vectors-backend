# TLDR

Documenting high-level steps of preparing project for YouTube video

- Used the `Agents Masterclass` repo as the starting point
- Adapted the repo to suit `noRagAgent`, `ragAgent`, & `reActAgent`
- Switched out `ChromaDB` for `Pinecone`
- Switching out `Redis` for `PostgreSQL`
- Adding basic application structure with auth and DB connection
- Refactored and removed unused code in both the frontend and backend repos
- Switching out `RedisChatMessageHistory` for `langchain-postgres`
  - https://github.com/langchain-ai/langchain-postgres
  ```.sh + psql + pseudocode
  docker run -it --rm --network agent-network postgres psql -h fullstack-pinecone -U postgres
  \l
  \c fullstack_pinecone
  \dt
  https://github.com/langchain-ai/langchain-postgres/blob/88831295acfb7bae3184c124ba82aaf2000dd3a9/langchain_postgres/chat_message_histories.py#L21
  CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                session_id UUID NOT NULL,
                message JSONB NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  );

  index_name = f"idx_{table_name}_session_id"

  CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} (session_id); √
  ```
- 
https://github.com/langchain-ai/langchain-postgres