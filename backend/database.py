"""
Database models and connection setup for Carbon Footprint Tracker.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from backend.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Transaction(Base):
    """Transaction model for storing purchase data."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    amount = Column(Float)
    category = Column(String)
    carbon_kg = Column(Float)
    confidence_score = Column(Float)
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class CarbonSuggestion(Base):
    """Model for storing AI-generated carbon reduction suggestions."""
    __tablename__ = "carbon_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    category = Column(String)
    suggestion = Column(String)
    potential_reduction_kg = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserProfile(Base):
    """User profile for tracking overall carbon footprint."""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    total_carbon_kg = Column(Float, default=0.0)
    monthly_carbon_kg = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    preferences = Column(JSON)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
