import psycopg

# Establish a synchronous connection to the database
# (or use psycopg.AsyncConnection for async)
conn_info = "host=0.0.0.0 port=5432 dbname=pinecone_demo user=<username> password=<password>"
conn_info = ... # Fill in with your connection info
sync_connection = psycopg.connect(conn_info)