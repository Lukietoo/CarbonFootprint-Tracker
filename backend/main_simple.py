"""
SIMPLIFIED Carbon Footprint Tracker Backend
Easy to understand version for learning!

This backend does 3 things:
1. Accept manual transaction entries (description, amount, category)
2. Calculate CO2 emissions using simple formulas
3. Store data in database for tracking over time
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel

from backend.database import get_db, init_db, Transaction, UserProfile

# Create the FastAPI app
app = FastAPI(title="Carbon Footprint Tracker - Simple Version")

# Allow frontend to talk to backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# SIMPLE CARBON CALCULATION
# No APIs needed - just basic math!
# ============================================

# How much CO2 per dollar spent in each category
# These are simple estimates (kg CO2 per $1 spent)
CARBON_ESTIMATES = {
    "food_meat": 0.8,        # Meat produces a lot of CO2
    "food_plant": 0.2,       # Plants produce less CO2
    "transportation": 0.5,   # Cars, buses, etc.
    "energy": 0.9,          # Electricity, gas
    "shopping": 0.3,        # General purchases
    "entertainment": 0.2,    # Movies, games, etc.
    "other": 0.25           # Default
}

def calculate_carbon(category: str, amount: float) -> float:
    """
    Simple function to estimate CO2 emissions

    Args:
        category: Type of purchase (food, transport, etc.)
        amount: How much money spent ($)

    Returns:
        Estimated kg of CO2 produced
    """
    # Get the CO2 rate for this category (or use 'other' as default)
    co2_per_dollar = CARBON_ESTIMATES.get(category, CARBON_ESTIMATES["other"])

    # Calculate: money spent × CO2 per dollar = total CO2
    total_co2 = amount * co2_per_dollar

    return round(total_co2, 2)


# ============================================
# DATA MODELS
# Define what data looks like
# ============================================

class TransactionInput(BaseModel):
    """What the user sends to add a transaction"""
    description: str        # What they bought (e.g., "Starbucks coffee")
    amount: float          # How much it cost (e.g., 5.50)
    category: str          # Type (e.g., "food_plant")
    date: str = None       # When (optional)
    user_id: str = "default_user"


class TransactionResponse(BaseModel):
    """What we send back to the user"""
    id: int
    description: str
    amount: float
    category: str
    carbon_kg: float       # The calculated CO2
    date: str

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Summary statistics for the dashboard"""
    total_carbon_kg: float           # Total CO2 ever
    monthly_carbon_kg: float         # CO2 this month
    transaction_count: int           # Number of purchases
    category_breakdown: dict         # CO2 by category


# ============================================
# API ENDPOINTS
# These are the URLs the frontend calls
# ============================================

@app.on_event("startup")
async def startup():
    """Run when the app starts - set up database"""
    init_db()


@app.get("/")
def home():
    """Home page - just returns a welcome message"""
    return {
        "message": "Carbon Footprint Tracker API - Simplified Version",
        "status": "running",
        "tip": "This version is easy to understand!"
    }


@app.post("/api/transactions", response_model=TransactionResponse)
async def add_transaction(
    transaction: TransactionInput,
    db: Session = Depends(get_db)
):
    """
    Add a new purchase to track

    User sends: description, amount, category
    We calculate: CO2 emissions
    We save: everything to database
    We return: the saved transaction with CO2
    """
    # Calculate CO2 for this purchase
    carbon_kg = calculate_carbon(transaction.category, transaction.amount)

    # Use provided date or today
    transaction_date = transaction.date if transaction.date else datetime.now().isoformat()

    # Create database record
    db_transaction = Transaction(
        user_id=transaction.user_id,
        description=transaction.description,
        amount=transaction.amount,
        date=datetime.fromisoformat(transaction_date.replace('Z', '+00:00')),
        category=transaction.category,
        carbon_kg=carbon_kg,
        confidence_score=1.0,  # We're confident in manual entry
        raw_data={}
    )

    # Save to database
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    # Update user's total carbon
    await update_user_total(transaction.user_id, db)

    return db_transaction


@app.get("/api/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Get all transactions for a user
    Returns: List of all purchases with CO2 data
    """
    transactions = db.query(Transaction)\
        .filter(Transaction.user_id == user_id)\
        .order_by(Transaction.date.desc())\
        .all()

    return transactions


@app.get("/api/dashboard", response_model=DashboardStats)
async def get_dashboard(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Get summary statistics for dashboard

    Calculates:
    - Total CO2 all time
    - CO2 this month
    - Number of transactions
    - Breakdown by category
    """
    # Get all transactions for this user
    transactions = db.query(Transaction)\
        .filter(Transaction.user_id == user_id)\
        .all()

    # Calculate total CO2
    total_carbon = sum(t.carbon_kg for t in transactions)

    # Calculate this month's CO2
    thirty_days_ago = datetime.now() - timedelta(days=30)
    monthly_transactions = [t for t in transactions if t.date >= thirty_days_ago]
    monthly_carbon = sum(t.carbon_kg for t in monthly_transactions)

    # Break down by category
    category_breakdown = {}
    for transaction in transactions:
        category = transaction.category
        if category not in category_breakdown:
            category_breakdown[category] = 0
        category_breakdown[category] += transaction.carbon_kg

    # Round all values
    category_breakdown = {k: round(v, 2) for k, v in category_breakdown.items()}

    return {
        "total_carbon_kg": round(total_carbon, 2),
        "monthly_carbon_kg": round(monthly_carbon, 2),
        "transaction_count": len(transactions),
        "category_breakdown": category_breakdown
    }


@app.get("/api/suggestions")
async def get_suggestions(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Get simple tips to reduce carbon footprint
    No AI needed - just helpful suggestions!
    """
    # Get user's transactions to see what they buy
    transactions = db.query(Transaction)\
        .filter(Transaction.user_id == user_id)\
        .all()

    if not transactions:
        return []

    # Calculate totals by category
    category_totals = {}
    for t in transactions:
        if t.category not in category_totals:
            category_totals[t.category] = 0
        category_totals[t.category] += t.carbon_kg

    # Find top 3 categories
    top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]

    # Simple suggestions based on top categories
    suggestions = []
    suggestion_map = {
        "food_meat": {
            "suggestion": "Try Meatless Mondays - skip meat one day per week",
            "reduction_kg": category_totals.get("food_meat", 0) * 0.15,
            "difficulty": "easy"
        },
        "food_plant": {
            "suggestion": "Buy local, seasonal produce to reduce transportation emissions",
            "reduction_kg": category_totals.get("food_plant", 0) * 0.10,
            "difficulty": "easy"
        },
        "transportation": {
            "suggestion": "Use public transport or carpool when possible",
            "reduction_kg": category_totals.get("transportation", 0) * 0.25,
            "difficulty": "medium"
        },
        "energy": {
            "suggestion": "Switch to LED bulbs and unplug devices when not in use",
            "reduction_kg": category_totals.get("energy", 0) * 0.20,
            "difficulty": "easy"
        },
        "shopping": {
            "suggestion": "Buy second-hand or choose quality items that last longer",
            "reduction_kg": category_totals.get("shopping", 0) * 0.15,
            "difficulty": "easy"
        },
    }

    # Create suggestions for top categories
    for category, carbon in top_categories:
        if category in suggestion_map:
            suggestion = suggestion_map[category].copy()
            suggestion["category"] = category
            suggestions.append(suggestion)

    return suggestions[:5]  # Return max 5 suggestions


@app.delete("/api/reset-data")
async def reset_data(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Delete all data for a user (start fresh)
    """
    deleted = db.query(Transaction)\
        .filter(Transaction.user_id == user_id)\
        .delete()

    db.commit()

    return {
        "message": f"Deleted {deleted} transactions",
        "deleted_count": deleted
    }


@app.post("/api/sample-data")
async def load_sample_data(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """
    Load some example data to see how the app works
    """
    # First, delete existing data
    db.query(Transaction).filter(Transaction.user_id == user_id).delete()
    db.commit()

    # Sample transactions
    samples = [
        {"description": "Starbucks Coffee", "amount": 5.50, "category": "food_plant"},
        {"description": "Uber Ride", "amount": 15.00, "category": "transportation"},
        {"description": "Burger King", "amount": 12.00, "category": "food_meat"},
        {"description": "Netflix Subscription", "amount": 15.99, "category": "entertainment"},
        {"description": "Electricity Bill", "amount": 85.00, "category": "energy"},
        {"description": "Amazon Shopping", "amount": 45.00, "category": "shopping"},
        {"description": "Chipotle Bowl", "amount": 11.50, "category": "food_plant"},
        {"description": "Gas Station", "amount": 40.00, "category": "transportation"},
    ]

    added = []
    for sample in samples:
        carbon_kg = calculate_carbon(sample["category"], sample["amount"])

        db_transaction = Transaction(
            user_id=user_id,
            description=sample["description"],
            amount=sample["amount"],
            date=datetime.now(),
            category=sample["category"],
            carbon_kg=carbon_kg,
            confidence_score=1.0,
            raw_data={}
        )

        db.add(db_transaction)
        added.append({
            "description": sample["description"],
            "carbon_kg": carbon_kg
        })

    db.commit()

    return {
        "message": f"Loaded {len(added)} sample transactions",
        "transactions": added
    }


# ============================================
# HELPER FUNCTIONS
# ============================================

async def update_user_total(user_id: str, db: Session):
    """Update the user's total carbon footprint"""
    # Get or create user profile
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)

    # Calculate total from all transactions
    total = db.query(Transaction)\
        .filter(Transaction.user_id == user_id)\
        .all()

    profile.total_carbon_kg = sum(t.carbon_kg for t in total)
    profile.last_updated = datetime.now()

    db.commit()
