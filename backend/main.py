"""
FastAPI backend for Carbon Footprint Tracker.
Main application with all API endpoints.
"""
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json

from backend.database import get_db, init_db, Transaction, UserProfile, CarbonSuggestion
from backend.classifier import TransactionClassifier
from backend.carbon_estimator import CarbonEstimator
from backend.suggestion_generator import SuggestionGenerator
from backend.transaction_parser import TransactionParser
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Carbon Footprint Tracker API",
    description="API for tracking and analyzing carbon footprint from purchases",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
classifier = TransactionClassifier()
carbon_estimator = CarbonEstimator()
suggestion_generator = SuggestionGenerator()
transaction_parser = TransactionParser()


# Pydantic models for API
class TransactionInput(BaseModel):
    description: str
    amount: float
    date: Optional[str] = None
    user_id: str = "default_user"


class TransactionResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    carbon_kg: float
    confidence_score: float
    date: datetime


class DashboardStats(BaseModel):
    total_carbon_kg: float
    monthly_carbon_kg: float
    transaction_count: int
    category_breakdown: dict
    top_category: str
    comparison_to_average: dict


class SuggestionResponse(BaseModel):
    suggestion: str
    reduction_kg: float
    difficulty: str
    category: str


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


# Health check
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": "Carbon Footprint Tracker",
        "version": "1.0.0"
    }


# Transaction endpoints
@app.post("/api/transactions/upload", response_model=List[TransactionResponse])
async def upload_transactions(
    file: UploadFile = File(...),
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Upload and process transactions from CSV file.
    """
    try:
        # Read file content
        content = await file.read()

        # Parse transactions
        parsed_transactions = transaction_parser.parse_csv(content)
        validated_transactions = transaction_parser.validate_transactions(parsed_transactions)

        # Process each transaction
        results = []
        for trans in validated_transactions:
            # Classify transaction
            category, confidence, estimated_carbon = classifier.classify(
                trans["description"],
                trans["amount"]
            )

            # Get more accurate carbon estimate
            carbon_data = await carbon_estimator.estimate_from_category(
                category,
                trans["amount"]
            )

            # Create database record
            db_transaction = Transaction(
                user_id=user_id,
                description=trans["description"],
                amount=trans["amount"],
                date=trans["date"],
                category=category,
                carbon_kg=carbon_data["carbon_kg"],
                confidence_score=confidence,
                raw_data=trans["raw_data"]
            )
            db.add(db_transaction)
            db.commit()
            db.refresh(db_transaction)

            results.append(TransactionResponse(
                id=db_transaction.id,
                description=db_transaction.description,
                amount=db_transaction.amount,
                category=db_transaction.category,
                carbon_kg=db_transaction.carbon_kg,
                confidence_score=db_transaction.confidence_score,
                date=db_transaction.date
            ))

        # Update user profile
        await update_user_carbon_total(user_id, db)

        return results

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


@app.post("/api/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionInput,
    db: Session = Depends(get_db)
):
    """
    Create a single transaction manually.
    """
    # Classify transaction
    category, confidence, _ = classifier.classify(
        transaction.description,
        transaction.amount
    )

    # Estimate carbon
    carbon_data = await carbon_estimator.estimate_from_category(
        category,
        transaction.amount
    )

    # Parse date
    trans_date = datetime.utcnow()
    if transaction.date:
        try:
            trans_date = datetime.fromisoformat(transaction.date)
        except:
            pass

    # Create database record
    db_transaction = Transaction(
        user_id=transaction.user_id,
        description=transaction.description,
        amount=transaction.amount,
        date=trans_date,
        category=category,
        carbon_kg=carbon_data["carbon_kg"],
        confidence_score=confidence,
        raw_data={}
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    # Update user profile
    await update_user_carbon_total(transaction.user_id, db)

    return TransactionResponse(
        id=db_transaction.id,
        description=db_transaction.description,
        amount=db_transaction.amount,
        category=db_transaction.category,
        carbon_kg=db_transaction.carbon_kg,
        confidence_score=db_transaction.confidence_score,
        date=db_transaction.date
    )


@app.get("/api/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    user_id: str = "default_user",
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all transactions for a user.
    """
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.date.desc()).limit(limit).all()

    return [
        TransactionResponse(
            id=t.id,
            description=t.description,
            amount=t.amount,
            category=t.category,
            carbon_kg=t.carbon_kg,
            confidence_score=t.confidence_score,
            date=t.date
        )
        for t in transactions
    ]


# Dashboard endpoints
@app.get("/api/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics for a user.
    """
    # Get all transactions
    all_transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()

    if not all_transactions:
        return DashboardStats(
            total_carbon_kg=0,
            monthly_carbon_kg=0,
            transaction_count=0,
            category_breakdown={},
            top_category="none",
            comparison_to_average={"status": "no_data"}
        )

    # Calculate total carbon
    total_carbon = sum(t.carbon_kg for t in all_transactions)

    # Calculate monthly carbon (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    monthly_transactions = [t for t in all_transactions if t.date >= thirty_days_ago]
    monthly_carbon = sum(t.carbon_kg for t in monthly_transactions)

    # Category breakdown
    category_breakdown = {}
    for t in all_transactions:
        category_breakdown[t.category] = category_breakdown.get(t.category, 0) + t.carbon_kg

    # Top category
    top_category = max(category_breakdown.items(), key=lambda x: x[1])[0] if category_breakdown else "none"

    # Comparison to average (US average is ~16 tons/year or ~1,333 kg/month)
    us_avg_monthly = 1333
    comparison = {
        "user_monthly_kg": monthly_carbon,
        "average_monthly_kg": us_avg_monthly,
        "difference_kg": monthly_carbon - us_avg_monthly,
        "percentage": ((monthly_carbon / us_avg_monthly) * 100) if us_avg_monthly > 0 else 0,
        "status": "below_average" if monthly_carbon < us_avg_monthly else "above_average"
    }

    return DashboardStats(
        total_carbon_kg=round(total_carbon, 2),
        monthly_carbon_kg=round(monthly_carbon, 2),
        transaction_count=len(all_transactions),
        category_breakdown={k: round(v, 2) for k, v in category_breakdown.items()},
        top_category=top_category,
        comparison_to_average=comparison
    )


# Suggestion endpoints
@app.get("/api/suggestions", response_model=List[SuggestionResponse])
async def get_suggestions(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Get personalized carbon reduction suggestions.
    """
    # Get recent transactions
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.date.desc()).limit(50).all()

    if not transactions:
        # Return generic suggestions
        return [
            SuggestionResponse(
                suggestion="Start tracking your purchases to get personalized suggestions",
                reduction_kg=0,
                difficulty="easy",
                category="general"
            )
        ]

    # Calculate category breakdown
    category_breakdown = {}
    total_carbon = 0
    for t in transactions:
        category_breakdown[t.category] = category_breakdown.get(t.category, 0) + t.carbon_kg
        total_carbon += t.carbon_kg

    # Generate suggestions
    trans_dicts = [
        {
            "description": t.description,
            "amount": t.amount,
            "category": t.category,
            "carbon_kg": t.carbon_kg
        }
        for t in transactions
    ]

    suggestions = await suggestion_generator.generate_suggestions(
        trans_dicts,
        total_carbon,
        category_breakdown
    )

    return [
        SuggestionResponse(
            suggestion=s["suggestion"],
            reduction_kg=s.get("reduction_kg", 0),
            difficulty=s.get("difficulty", "medium"),
            category=s.get("category", "general")
        )
        for s in suggestions
    ]


# Sample data endpoint
@app.post("/api/sample-data")
async def load_sample_data(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Load sample transaction data for demo purposes.
    """
    sample_transactions = transaction_parser.create_sample_data()

    results = []
    for trans in sample_transactions:
        # Classify transaction
        category, confidence, _ = classifier.classify(
            trans["description"],
            trans["amount"]
        )

        # Estimate carbon
        carbon_data = await carbon_estimator.estimate_from_category(
            category,
            trans["amount"]
        )

        # Create database record
        db_transaction = Transaction(
            user_id=user_id,
            description=trans["description"],
            amount=trans["amount"],
            date=trans["date"],
            category=category,
            carbon_kg=carbon_data["carbon_kg"],
            confidence_score=confidence,
            raw_data={}
        )
        db.add(db_transaction)
        results.append({
            "description": trans["description"],
            "carbon_kg": carbon_data["carbon_kg"]
        })

    db.commit()

    # Update user profile
    await update_user_carbon_total(user_id, db)

    return {
        "message": f"Loaded {len(results)} sample transactions",
        "transactions": results
    }


# Helper functions
async def update_user_carbon_total(user_id: str, db: Session):
    """Update user's total carbon footprint."""
    # Get or create user profile
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)

    # Calculate totals
    all_transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    total_carbon = sum(t.carbon_kg for t in all_transactions)

    # Calculate monthly carbon
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    monthly_transactions = [t for t in all_transactions if t.date >= thirty_days_ago]
    monthly_carbon = sum(t.carbon_kg for t in monthly_transactions)

    # Update profile
    profile.total_carbon_kg = total_carbon
    profile.monthly_carbon_kg = monthly_carbon
    profile.last_updated = datetime.utcnow()

    db.commit()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
