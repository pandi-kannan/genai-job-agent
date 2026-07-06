import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True)
    job_title = Column(String(255))
    company_name = Column(String(255))
    resume_gaps = Column(Text)
    suggested_bullets = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(engine)

def save_analysis(job_title, company_name, resume_gaps, suggested_bullets):
    session = SessionLocal()
    record = Analysis(
        job_title=job_title,
        company_name=company_name,
        resume_gaps=resume_gaps,
        suggested_bullets=suggested_bullets
    )
    session.add(record)
    session.commit()
    session.close()

def get_all_analyses():
    session = SessionLocal()
    records = session.query(Analysis).order_by(Analysis.created_at.desc()).all()
    session.close()
    return records

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")