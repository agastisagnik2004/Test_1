from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:Sagnik%40052004@127.0.0.1:5432/student_db"

engine = create_engine(
    DATABASE_URL,
    echo=True   
  )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
