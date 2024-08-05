from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQL_ALCHEMY_DATABASE_URL = 'sqlite:///workout_app.db'
SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:mysecretpassword@fullstack-pinecone:5432/fullstack_pinecone'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()